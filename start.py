import multiprocessing
import os
import logging
from signalrcore.hub_connection_builder import HubConnectionBuilder

from modbusConnection import ModbusConnection
from model import DriverDetail
import time, logging

from process import ModBusProcess
from multiprocessing import Process

from signalRProcess import SignalRProcess

logger = logging.getLogger('app_logger')


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

class ModBusProcessManager:
    clients = []  # {client: Modbus client, slave, port, host, isOpen, isClosed}
    demo = []
    driverDetails = []  # {  slave, port, host etc}
    processes = []
    osProcesses = []



    def __init__(self):
        self.appended_processes = set()
        self.fetchDriverDetails()
        self.createProcesses()
        self.startWork()



    def fetchDriverDetails(self):
        try:
            self.driverDetails = DriverDetail().find_all_driver_detail()
            print("Driver List", self.driverDetails)
            logger.info(f'Create Process{self.driverDetails}')

        except Exception as ex:
            logger.error(f'Driver data error')
            logger.exception(ex)

    def createProcesses(self):
        for driverDetail in self.driverDetails:

            Active = driverDetail[12]
            Critical = driverDetail[14]
            Frequency = driverDetail[2]
            if Active:
                client = ModbusConnection(driverDetail[10], driverDetail[4], driverDetail[3]).connection()
                self.clients.append({
                    "client": client,
                    "id": driverDetail[0]
                })

                if Critical:
                    criticalProcess = SignalRProcess(driverDetail[0], client, Frequency, signalRConnection())
                    self.processes.append(criticalProcess)
                else:
                    process = ModBusProcess(driverDetail[0], client, Frequency)
                    self.processes.append(process)
                    print("Create Process", len(self.processes))
                    logger.info(f'"Create Process", len(self.processes)')

    def startWork(self):

        while True:

            # for c in self.clients:
            #     try:
            #         if not c["client"].open():
            #             driverDetails = [d for d in self.driverDetails if d[0] == c["id"]][0]
            #             print("driverDetails", driverDetails)
            #             c["client"] = ModbusConnection(driverDetails[10], driverDetails[4],
            #                                            driverDetails[3]).connection()
            #     except Exception as ex:
            #         logger.error(ex)

            print("process", len(self.processes))

            for ap in self.processes:
                if ap not in self.appended_processes:
                    print("OS Process Append")

                    os_process = multiprocessing.Process(target=ap.startConnection)
                    os_process.start()
                    self.osProcesses.append(os_process)
                    self.appended_processes.add(ap)

            print("OS process", len(self.osProcesses))
            for p in self.osProcesses:
                try:

                    if not p.is_alive():
                        print("OS Process start")
                        p.start()  # this is OS's start method
                except Exception as ex:
                    logger.error("Process start error")
                    logger.exception(ex)

            # for p in self.osProcesses:
            #     p.join(timeout=0)
            #
            time.sleep(1)
