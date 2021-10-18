"""
-*- coding: utf-8 -*-
@Time    : 18/10/2021 19:53
@Author  : Thu Ra
@Email   : thura747@gmail.com
@File    : Utilities.py
@Software: PyCharm
"""

from datetime import datetime, time

import enum

import sqlite_db_connection


class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


class Utilities:

    def __init__(self, download_list_file, unit=SIZE_UNIT.MB):
        self.download_list_file = download_list_file
        self.unit = unit
        self.file_size = 0
        self.data = None
        self.db = sqlite_db_connection.Database()

    def convert_unit(self, size_in_bytes):
        """ Convert the size from bytes to other units like KB, MB or GB"""
        if self.unit == SIZE_UNIT.KB:
            return size_in_bytes / 1024
        elif self.unit == SIZE_UNIT.MB:
            return size_in_bytes / (1024 * 1024)
        elif self.unit == SIZE_UNIT.GB:
            return size_in_bytes / (1024 * 1024 * 1024)
        else:
            return size_in_bytes

    def downloading_list(self):
        """ appending the key from csv file to list
        :return:
        """
        file1 = open(self.download_list_file, 'r')
        lines = file1.readlines()
        mf_keys = []
        for line in lines:
            mf_keys.append(line)

        return mf_keys

    def check_key(self, key):
        """ check the key is exists in database.
        :return:
        """
        sql = '''SELECT * FROM media_files WHERE m_key = ?'''
        params = (key,)
        rows = self.db.run_select_query(sql, params)

        if not rows:
            return False
        return True

    def inserting_record(self, data):
        """ inserting the records into database
        :data: data into table
        :return:
        """

        # checking the key before inserting into table
        if not self.check_key(data['key']):
            sql = '''INSERT INTO media_files (name, m_key, m_size, m_unit, m_date) VALUES (?, ?, ?, ?, ?)'''
            params = (
                data['name'], data['key'], round(self.convert_unit(int(data['size'])), 2), self.unit.name,
                datetime.now())
            self.db.run_insert_update_query(sql, params)
