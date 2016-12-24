import sqlite3
import os
import MySQLdb
from utils.logger import debug


class DataSource(object):
    __DATA_SOURCE = None

    __SQL_TYPE = "mysql"

    #def __init__(self, db):
    #    self.db = db

    def query_for_object(self, domain_type=None, query=None, *args):
        cursor = self.db.cursor()
        cursor.execute(query, args)
        rows = cursor.fetchall()
        domain = domain_type()
        domain.fill(rows[0])
        return domain

    def query_for_dictionary(self, domain_type=None, query=None, *args):
        dictionary = {}
        cursor = self.db.cursor()
        cursor.execute(query, args)
        rows = cursor.fetchall()
        for row in rows:
            domain = domain_type()
            domain.fill(row)
            dictionary[domain.id] = domain
        return dictionary

    def query_for_list(self, domain_type=None, query=None, *args):
        list_objects = []
        cursor = self.db.cursor()
        cursor.execute(query, args)
        rows = cursor.fetchall()
        for row in rows:
            domain = domain_type()
            domain.fill(row)
            list_objects.append(domain)
        return list_objects

    def get_rows(self, query, *args):
        cursor = self.db.cursor()
        cursor.execute(query, args)
        self.db.commit()
        return cursor.fetchall()

    def execute(self, query, args=[]):
        cursor = self.db.cursor()
        cursor.execute(query, args)
        self.db.commit()

    @staticmethod
    def get_instance():
        if DataSource.__DATA_SOURCE is not None:
            return DataSource.__DATA_SOURCE
        if DataSource.__SQL_TYPE == "mysql":
            DataSource.__DATA_SOURCE = MysqlDataSource()
        else:
            DataSource.__DATA_SOURCE = SQLiteDataSource()
        return DataSource.__DATA_SOURCE

    @staticmethod
    def set_sql_type(sql_type):
        DataSource.__SQL_TYPE = sql_type


class MysqlDataSource(DataSource):

    def __init__(self):
        self.db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                             user="root",  # your username
                             passwd="root",  # your password
                             db="domotica")
        self.db.autocommit(True)


class SQLiteDataSource(DataSource):
    __CALLS = 0

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = base_dir.replace("batch", "")
        __DATABASE_PATH = os.path.join(base_dir, 'db.sqlite3')
        self.db = sqlite3.connect(__DATABASE_PATH)

    def execute(self, query, *args):
        query = query.replace("%s", "?")
        super(SQLiteDataSource, self).execute(query, *args)

    def query_for_object(self, domain_type=None, query=None, *args):
        query = query.replace("%s", "?")
        return super(SQLiteDataSource, self).query_for_object(domain_type, query, *args)

    def query_for_list(self, domain_type=None, query=None, *args):
        query = query.replace("%s", "?")
        return super(SQLiteDataSource, self).query_for_list(domain_type, query, *args)


    @staticmethod
    def get_instance():
        return DataSource()
