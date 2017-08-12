import sqlite3
import os
import pandas as pd
from threading import Timer
from serial_utils import serial_reslut
from contextlib import closing

def connect_db():
    return sqlite3.connect("housemonitor.db")

def init_db():
    with closing(connect_db()) as db:
        db.cursor().execute("create table entries (id integer primary key autoincrement,record_time datetime default (datetime('now', 'localtime')),temperature float,humidity float,pm_2_5 integer,pm_10 integer, formaldehyde integer);")
        db.commit()

if not os.path.exists('housemonitor.db'):
    init_db()

def recordData():
    conn = sqlite3.connect('housemonitor.db')
    c = conn.cursor()
    if serial_reslut['status'] == 'initialized':
        value = (serial_reslut['tmp'], serial_reslut['hum'], serial_reslut['pm_2_5'], serial_reslut['pm_10'],serial_reslut['CH2O'])
        insert_sql = "insert into entries (temperature, humidity, pm_2_5, pm_10, formaldehyde) values(?,?,?,?,?);"
        c.execute(insert_sql, value)
        conn.commit()
        conn.close()
    t = Timer(1800, recordData)
    t.start()

recordData()

def getDate(entry, duration):
    con = sqlite3.connect('housemonitor.db')
    df = pd.read_sql_query("SELECT * from entries WHERE record_time > datetime('now', 'localtime', '-" + duration + " hours')",con)
    con.close()
    record_time = df['record_time'].values.tolist()
    values = df[entry].values.tolist()
    for i in range(len(record_time)):
       record_time[i] = record_time[i].encode('utf-8')

    return values, record_time

