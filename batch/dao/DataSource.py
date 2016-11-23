import sqlite3
import os


class DataSource(object):

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = base_dir.replace("batch", "")
        data_base_path = os.path.join(base_dir, 'db.sqlite3')
        self.db = sqlite3.connect(data_base_path)

    def get_rows(self, query, *args):
        cursor = self.db.cursor()
        cursor.execute(query, args)
        return cursor.fetchall()

    def execute(self, query, *args):
        cursor = self.db.cursor()
        cursor.execute(query, args)
        self.db.commit()
