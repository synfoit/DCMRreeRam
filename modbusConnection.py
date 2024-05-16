from pyModbusTCP.client import ModbusClient


class ModbusConnection:

    def __init__(self, slav_id, NetworkAddress, Port):
        self.NetworkAddress = NetworkAddress
        self.Port = Port
        self.SlavID = slav_id
        self.auto_open = False
        self.auto_close = False
        self.modbus_client = ModbusClient()

    def connection(self):
        self.modbus_client = ModbusClient(host=self.NetworkAddress, port=int(self.Port), unit_id=int(self.SlavID))
        # self.modbus_client.open()
        return self.modbus_client

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.modbus_client.close()
