import time, logging

from customsMethod import structpack, structunPack, currentDateTime
from model import TagMasterModel, TagModel, DeviceConnectionLog


logger = logging.getLogger('app_logger')


class ModBusProcess:

    def __init__(self, DriverDetailID, modbus_client, Frequency):
        self.id = DriverDetailID
        self.DriverDetailID = DriverDetailID
        self.modbus_client = modbus_client
        self.Frequency = Frequency

    def logException(self, ex):
        logger.exception(ex)
        DeviceConnectionLog().insert(self.DriverDetailID, False,
                                     'Client Closed with Exception ' + str(ex),
                                     currentDateTime())

    def startConnection(self):
        print('modbus process')
        try:
            if self.modbus_client.open():
                self.readTags()
            else:
                logger.info(f"Could not read tags as connection is not open for {self.DriverDetailID}")
                print(f"Could not read tags as connection is not open for {self.DriverDetailID}")

        except Exception as ex:
            logger.error(f'initProcess: An error modbus Server at {ex}, while starting process.')
            print(f'initProcess: An error modbus Server at {ex}, while starting process.')


    def readTags(self):
        tag_list = TagMasterModel().find_by_DriverDetailID(self.DriverDetailID)
        print("tag_list",tag_list)
        while True:
            datetime = currentDateTime()
            tag_db_value_list = []

            try:

                for tag_data in tag_list:

                    logger.info(f'readTags: Driver {self.DriverDetailID} tag_data{tag_data}')
                    data = ""
                    packed_string = ""

                    if tag_data[5] == 'INPUT REGISTER':
                        data = self.modbus_client.read_input_registers(int(tag_data[3]), int(tag_data[4]))
                        print("data",data)

                    elif tag_data[5] == 'HOLDING REGISTER':
                        data = self.modbus_client.read_holding_registers(int(tag_data[3]), int(tag_data[4]))

                    if tag_data[7] == 'NO' and data != "" and data is not None:
                        packed_string = structpack(data[0], data[1])

                    elif tag_data[7] == 'YES' and data != "" and data is not None:
                        packed_string = structpack(data[1], data[0])
                    print("packed_string", packed_string)
                    if len(packed_string) != 0:
                        tag_value = structunPack(packed_string)
                        logger.info(f'Driver tag_data{tag_data} value {tag_value}')
                        print(f'Driver tag_data{tag_data} value {tag_value}')
                        if tag_data[9] == 'YES' and tag_value != 'nan':

                            tag_value_ = (tag_data[0], tag_value, datetime)
                            tag_db_value_list.append(tag_value_)

                if len(tag_db_value_list) != 0:
                    print("tag_db_value_list", str(tag_db_value_list))
                    TagModel().insert_multiple(tag_db_value_list)
                    logger.info(
                        f'tag_db_value_list {str(tag_db_value_list)} Server at:'
                        f' {self.modbus_client.host}/{self.modbus_client.port}')

            except Exception as ex:
                print(ex)
                self.modbus_client.close()

            time.sleep(60)
