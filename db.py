import sqlite3
from tkinter.constants import E

class Database:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cur = self.connection.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS meets (id INTEGER PRIMARY KEY, meet_name text NOT NULL UNIQUE, s_date text, e_date text, meet_link text)")
        self.connection.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM meets")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self,meet_name,s_date,e_date, meet_link):
        self.cur.execute("INSERT INTO meets VALUES(NULL,?,?,?,?)",(meet_name,s_date,e_date, meet_link))
        self.connection.commit()
    
    def remove(self,id):
        self.cur.execute("DELETE FROM meets WHERE id = ?", (id,))
        self.connection.commit()
    
    def update(self,id,meet_name,s_date,e_date, meet_link):
        self.cur.execute("UPDATE meets SET meet_name = ?, s_date = ?, e_date = ?, meet_link = ? WHERE id = ?", (meet_name,s_date,e_date, meet_link,id))
        self.connection.commit()
    

    def __del__(self):
        self.connection.close()


db = Database('meets.db')
