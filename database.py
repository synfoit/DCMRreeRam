import pyodbc

import os
from dotenv import load_dotenv

load_dotenv()


class Database:

    def __init__(self):
        self.db_driver = os.getenv('DB_DRIVER')
        self.db_server = os.getenv('DB_SERVER')
        self.db_database = os.getenv('DB_DATABASE')
        self.db_uid = os.getenv('DB_UID')
        self.db_pwd = os.getenv('DB_PWD')
        self.connection_string = f"Driver={self.db_driver};Server={self.db_server};Database={self.db_database};UID={self.db_uid};PWD={self.db_pwd}; "
        print("dbconnection", self.connection_string)

        self.db_handle = pyodbc.connect(self.connection_string)
        self.mycursor = self.db_handle.cursor()

    def get_single_data(self, table, query_columns_dict):
        selection_list = " AND ".join([
            f"{column_name} {query_columns_dict[column_name][0]} ?"
            for column_name in sorted(query_columns_dict.keys())
        ])

        sql = f"SELECT * FROM {table} WHERE {selection_list}"

        val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        result = self.mycursor.fetchone()

        return result

    def get_multiple_data(self, table, query_columns_dict):

        if query_columns_dict is None:

            sql = f"SELECT * FROM {table}"
            self.mycursor.execute(sql)
        else:
            selection_list = " AND ".join([
                f"{column_name} {query_columns_dict[column_name][0]} ?"
                for column_name in sorted(query_columns_dict.keys())
            ])
            sql = f"SELECT * FROM {table} WHERE {selection_list} "

            val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))

            value = self.mycursor.execute(sql, val)

        result = self.mycursor.fetchall()

        return result

    def get_value_from_sp(self, argument):

        self.mycursor.execute(argument)
        return self.mycursor.fetchall()

    def get_multiple_data_orderby(self, table, query_columns_dict):

        if query_columns_dict is None:
            sql = f"SELECT * FROM {table}"
            self.mycursor.execute(sql)
        else:
            selection_list = " AND ".join([
                f"{column_name} {query_columns_dict[column_name][0]} ?"
                for column_name in sorted(query_columns_dict.keys())
            ])
            sql = f"SELECT * FROM {table} WHERE {selection_list} order by TagAddress"

            val = tuple(query_columns_dict[column_name][1] for column_name in sorted(query_columns_dict.keys()))

            self.mycursor.execute(sql, val)

        result = self.mycursor.fetchall()

        return result

    def insert_single_data(self, table, query_columns_dict):
        column_names = ",".join([f"{column_name}" for column_name in sorted(query_columns_dict.keys())])
        column_holders = ",".join([f"?" for column_name in sorted(query_columns_dict.keys())])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"

        val = tuple(query_columns_dict[column_name] for column_name in sorted(query_columns_dict.keys()))

        self.mycursor.execute(sql, val)
        self.db_handle.commit()

        return self.mycursor.rowcount

    def insert_multiple_data(self, table, columns, multiple_data):
        column_names = ",".join(columns)
        column_holders = ",".join([f"?" for column_name in columns])
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({column_holders})"

        self.mycursor.executemany(sql, multiple_data)
        self.db_handle.commit()

        return self.mycursor.rowcount

    def update_single_data(self, table, id, status):
        sql = f"UPDATE {table} SET Active ='{status}' Where DriverDetailID={id}"

        self.mycursor.execute(sql)
        self.db_handle.commit()

        return self.mycursor.rowcount
