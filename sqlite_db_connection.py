"""
-*- coding: utf-8 -*-
@Time    : 18/10/2021 19:00 PM
@Author  : Thu Ra
@Email   : thura747@gmail.com
@File    : sqlite.py
@Software: PyCharm
"""
import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self):
        database = "test_db2.db"
        self.conn = None
        self.cur = ""
        self.file_size = 0

        self.create_connection(database)
        self.create_media_files_table()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """

        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def create_media_files_table(self):
        """ sql statement to create media_files table
        :return:
        """
        sql_create_media_files_table = """ CREATE TABLE IF NOT EXISTS media_files (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                m_key text,
                                                m_size DECIMAL(10,2),
                                                m_unit text,
                                                m_date DATETIME
                                            ); """
        self.create_table(sql_create_media_files_table)

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(create_table_sql)
        except Error as e:
            print(e)

    def run_insert_update_query(self, sql, params):
        """ Insert and Update Query
        :sql: query statement
        :params: params to insert or update
        :return: inserted ID
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, params)
            self.conn.commit()
            return self.cur.lastrowid
        except Error as e:
            print(e)

    def run_select_query(self, sql, params):
        """ Select Query
        :sql: query statement
        :params: params to filter
        :return: fetch all rows
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, params)
            return self.cur.fetchall()
        except Error as e:
            print(e)
