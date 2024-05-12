import sqlite3

class Connection_manger:
    # Connect to SQLite database
    def __init__(self):
        self.conn = sqlite3.connect('metadata.db')
        self.c = self.conn.cursor()
        # Create tables for metadata and SKU data
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= 'metadata' ")
        self.result_meta = self.c.fetchone()
        if self.result_meta is None:
            self.c.execute('''CREATE TABLE metadata
                         (id INTEGER PRIMARY KEY, Location TEXT, Department TEXT, Category TEXT, SubCategory TEXT)''')
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= 'sku_data' ")
        self.result_sku = self.c.fetchone()
        if self.result_sku is None:
            self.c.execute('''CREATE TABLE sku_data
                         (id INTEGER PRIMARY KEY, SKU INTEGER, Name TEXT, Location TEXT, Department TEXT, Category TEXT, SubCategory TEXT)''')
        # Commit changes and close connection
        self.conn.commit()
        #self.conn.close()


