import sqlite3
import os
import threading


class DataSource(object):
    __DATA_SOURCE = None

    def __init__(self):
        self.lockDB = threading.Lock()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = base_dir.replace("batch", "")
        data_base_path = os.path.join(base_dir, 'db.sqlite3')
        self.db = sqlite3.connect(data_base_path)

    def query_for_object(self, domain_type=None, query=None, *args):
        with self.lockDB:
            cursor = self.db.cursor()
            cursor.execute(query, args)
            rows = cursor.fetchall()
            domain = domain_type()
            return domain.fill(rows[0])

    def query_for_dictionary(self, domain_type=None, query=None, *args):
        with self.lockDB:
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
        with self.lockDB:
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
        with self.lockDB:
            cursor = self.db.cursor()
            cursor.execute(query, args)
            return cursor.fetchall()

    def execute(self, query, *args):
        with self.lockDB:
            cursor = self.db.cursor()
            cursor.execute(query, args)
            self.db.commit()

    @staticmethod
    def get_instance():
        if DataSource.__DATA_SOURCE is None:
            DataSource.__DATA_SOURCE = DataSource()

        return DataSource.__DATA_SOURCE

