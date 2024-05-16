import os
import time

from customsMethod import structpack, structunPack, currentDateTime
from model import TagMasterModel, DeviceConnectionLog

import logging
from signalrcore.hub_connection_builder import HubConnectionBuilder

logger = logging.getLogger('app_logger')


def getData(tag_list, Value_list, modbus_client):
    for i in range(len(tag_list)):
        tag_value = ""
        data = ""
        packed_string = ""

        if tag_list[i][5] == 'INPUT REGISTER':
            data = modbus_client.read_input_registers(int(tag_list[i][3]), int(tag_list[i][4]))

        elif tag_list[i][5] == 'HOLDING REGISTER':
            data = modbus_client.read_holding_registers(int(tag_list[i][3]), int(tag_list[i][4]))

        if tag_list[i][7] == 'NO' and data != "" and data is not None:
            packed_string = structpack(data[0], data[1])

        elif tag_list[i][7] == 'YES' and data != "" and data is not None:
            packed_string = structpack(data[1], data[0])

        if len(packed_string) != 0:
            tag_value = structunPack(packed_string)

        tag_value_array = Value_list[i]["data"]

        if len(tag_value_array) < 5:
            tag_value_array.append(tag_value)

        elif len(tag_value_array) == 5:
            tag_value_array.pop(0)
            tag_value_array.append(tag_value)

    return Value_list


def signalRConnection():
    server_url = os.getenv('SignalRURL')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    hub_connection = HubConnectionBuilder() \
        .with_url(server_url, options={"verify_ssl": False}) \
        .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
        .with_automatic_reconnect({
        "type": "interval",
        "keep_alive_interval": 10,
        "intervals": [1, 3, 5, 6, 7, 87, 3]
    }).build()

    hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
    hub_connection.on_error(lambda: print("error has occurred"))
    hub_connection.on_close(lambda: print("connection closed"))

    hub_connection.on("ReceiveMessage", print)
    hub_connection.start()

    return hub_connection


class SignalRProcess:

    def __init__(self, DriverDetailID, modbus_client, Frequency, signalRConnection):
        self.id = DriverDetailID
        self.DriverDetailID = DriverDetailID
        self.modbus_client = modbus_client
        self.Frequency = Frequency
        self.signalRConnection = signalRConnection

    def logException(self, ex):
        logger.exception(ex)
        DeviceConnectionLog().insert(self.DriverDetailID, False,
                                     'Client Closed with Exception' + str(ex),
                                     currentDateTime())

    def startConnection(self):
        print("signalR")
        try:
            if self.modbus_client.open():
                self.readTags()
            else:
                logger.info(f"Could not read tags as connection is not open for {self.DriverDetailID}")

        except Exception as ex:
            logger.error(f'initProcess: An error modbus Server at {ex}, while starting process.')
            self.logException(ex)
            self.modbus_client.close()

    def readTags(self):
        print("driverNumber",self.DriverDetailID)
        Voltage_tag_list = TagMasterModel().find_by_DriverDetailID_and_Name(self.DriverDetailID, 'Voltage%')
        Current_tag_list = TagMasterModel().find_by_DriverDetailID_and_Name(self.DriverDetailID, 'Current%')
        PowerFactor_tag_list = TagMasterModel().find_by_DriverDetailID_and_Name(self.DriverDetailID, 'PowerFactor%')
        KWH_tag_list = TagMasterModel().find_by_DriverDetailID_and_Name(self.DriverDetailID, 'KWh%')

        Voltage_list = []
        for Voltage_tag in Voltage_tag_list:
            Voltage_value = {
                'name': Voltage_tag[2],
                'data': []
            }
            Voltage_list.append(Voltage_value)

        Current_list = []
        for Current_tag in Current_tag_list:
            Current_value = {
                'name': Current_tag[2],
                'data': []
            }
            Current_list.append(Current_value)

        PowerFactor_list = []
        for PowerFactor_tag in PowerFactor_tag_list:
            PowerFactor_value = {
                'name': PowerFactor_tag[2],
                'data': []
            }
            PowerFactor_list.append(PowerFactor_value)

        KWH_list = []
        for KWH_tag in KWH_tag_list:
            KWH_value = {
                'name': KWH_tag[2],
                'data': []
            }
            KWH_list.append(KWH_value)

        Time_list = []
        hub_connection = self.signalRConnection

        while True:
            data_time = currentDateTime()

            try:
                logger.info(f'Modbus TCP To SignalR')
                print("for loop start", currentDateTime())

                P_list = getData(PowerFactor_tag_list, PowerFactor_list, self.modbus_client)
                K_list = getData(KWH_tag_list, KWH_list, self.modbus_client)

                if len(Time_list) < 5:
                    Time_list.append(data_time)

                elif len(Time_list) == 5:
                    Time_list.pop(0)
                    Time_list.append(data_time)

                V_list = getData(Voltage_tag_list, Voltage_list, self.modbus_client)
                C_list = getData(Current_tag_list, Current_list, self.modbus_client)

                message = {
                    'Id': self.DriverDetailID,
                    'Time': Time_list,
                    'Voltage_List': V_list,
                    'Current_List': C_list,
                    'PowerFactor_List': P_list,
                    'KWH_List': K_list

                }
                logger.info(f'Modbus TCP To SignalR message: {message} ')
                hub_connection.send("SendData", [[message]])

                print("for loop end", currentDateTime())

            except Exception as ex:
                hub_connection.stop()
                logger.error('error in signalR class')
                logger.exception(ex)
                print("exception", ex)

                DeviceConnectionLog().insert(self.DriverDetailID, False,
                                             'Client Closed with Exception',
                                             currentDateTime())

            time.sleep(60)
