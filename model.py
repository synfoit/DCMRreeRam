from database import Database

column_compare = {
    'EQUAL_TO': '=',
    'GREATER_THAN': '>',
    'GREATER_THAN_OR_EQUAL_TO': '>=',
    'LESSER_THAN': '<',
    'LESSER_THAN_OR_EQUAL_TO': '<=',
    'LIKE':'LIKE'
}


class DriverDetail:
    DriverDetail_TABLE = 'DriverDetail'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()

        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_driver_detail(self):
        result = self._db.get_multiple_data(DriverDetail.DriverDetail_TABLE, None)

        return result

    def find_all_driver_detail_sp(self, command):

        return self._db.get_value_from_sp(command)

    def find_driver_detail_id(self, device_id):
        query_columns_dict = {
            'DriverDetailID': (column_compare['EQUAL_TO'], device_id)
        }
        result = self._db.get_single_data(DriverDetail.DriverDetail_TABLE, query_columns_dict)
        return result

    def update_device_status(self, DriverDetailID, status):
        result = self._db.update_single_data(DriverDetail.DriverDetail_TABLE, DriverDetailID, status)
        return result


class DriverMaster:
    DriverMaster_TABLE = 'DriverMaster'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_by_DriverMasterID(self, driver_master_id):
        query_columns_dict = {
            'DriverMasterID': (column_compare['EQUAL_TO'], driver_master_id)
        }
        result = self._db.get_single_data(DriverMaster.DriverMaster_TABLE, query_columns_dict)
        return result

    def find_by_DriverMaster(self):
        result = self._db.get_multiple_data(DriverMaster.DriverMaster_TABLE, None)
        return result


class TagModel:
    TAG_TABLE = 'FloatTable'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_tag(self):
        result = self._db.get_multiple_data(TagModel.TAG_TABLE, None)
        return result

    def insert(self, tag_id, value, date_time):
        self.latest_error = ''

        query_columns_dict = {
            'TagId': tag_id,
            'TagValue': value,
            'DateandTime': date_time
        }
        print(query_columns_dict)

        row_count = self._db.insert_single_data(TagModel.TAG_TABLE, query_columns_dict)
        return row_count

    def insert_multiple(self, daily_report_docs):
        query_columns = [
            'TagId',
            'TagValue',
            'DateandTime'
        ]

        row_count = self._db.insert_multiple_data(TagModel.TAG_TABLE, query_columns, daily_report_docs)
        return row_count


class TagMasterModel:
    TagMaster_TABLE = 'TagMaster'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_tag(self):
        result = self._db.get_multiple_data(TagModel.TAG_TABLE, None)
        return result

    def find_by_DriverDetailID(self, driver_detail_id):
        query_columns_dict = {
            'DriverDetailID': (column_compare['EQUAL_TO'], driver_detail_id)
        }
        result = self._db.get_multiple_data_orderby(TagMasterModel.TagMaster_TABLE, query_columns_dict)
        return result

    def find_by_DriverDetailID_and_Name(self, driver_detail_id,TagName):
        query_columns_dict = {
            'DriverDetailID': (column_compare['EQUAL_TO'], driver_detail_id),
            'TagName': (column_compare['LIKE'], TagName)
        }

        result = self._db.get_multiple_data_orderby(TagMasterModel.TagMaster_TABLE, query_columns_dict)
        return result

    def find_by_TagID(self, TagID):
        query_columns_dict = {
            'TagID': (column_compare['EQUAL_TO'], TagID)
        }
        result = self._db.get_single_data(TagMasterModel.TagMaster_TABLE, query_columns_dict)
        return result


class DeviceConnectionLog:
    DeviceConnectionLog_TABLE = 'DeviceConnectionLog'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def find_all_driver_detail(self):
        result = self._db.get_multiple_data(DeviceConnectionLog.DeviceConnectionLog_TABLE, None)
        return result

    def find_driver_detail_id(self, device_id):
        query_columns_dict = {
            'DriverDetailID': (column_compare['EQUAL_TO'], device_id)
        }

        result = self._db.get_single_data(DeviceConnectionLog.DeviceConnectionLog_TABLE, query_columns_dict)

        return result

    def insert(self, DriverDetailID, IsConnect, Msg, date_time):
        self.latest_error = ''

        query_columns_dict = {
            'DriverDetailID': DriverDetailID,
            'IsConnect': IsConnect,
            'Msg': Msg,
            'DateTime': date_time
        }
        # print(query_columns_dict)

        row_count = self._db.insert_single_data(DeviceConnectionLog.DeviceConnectionLog_TABLE, query_columns_dict)
        return row_count

    def update_device_status(self, DriverDetailID, status):
        result = self._db.update_single_data(DeviceConnectionLog.DeviceConnectionLog_TABLE, DriverDetailID, status)
        return result


class DeviceException:
    DeviceException_TABLE = 'DeviceException'

    def __init__(self):
        # self._db_config = db_config
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    @latest_error.setter
    def latest_error(self, latest_error):
        self._latest_error = latest_error

    def insert(self, Msg, time, DriverDetailID):
        self.latest_error = ''

        query_columns_dict = {
            'exceptionMsg': Msg,
            'time': time,
            'deviceConnectionId': DriverDetailID
        }

        row_count = self._db.insert_single_data(DeviceException.DeviceException_TABLE, query_columns_dict)
        return row_count
