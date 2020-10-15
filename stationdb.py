
import sqlite3 as sl
con = sl.connect('becalm-station.db')
with con:
  con.execute("""
             CREATE TABLE measure (
               type char(1),
               value float,
               timestamp DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
               )
               """)
