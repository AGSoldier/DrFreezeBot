#!/usr/bin/env python3

import os
import sys
import psycopg2

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

upd_dir = os.path.join(sys.path[0], "updates/")
conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)

print("[INFO] UPDATING DATABASE")
with conn.cursor() as cur:
    for filename in os.listdir(upd_dir):
        print("[INFO] LAUNCHING FILE {}".format(filename))
        try:
            cur.execute(open(os.path.join(upd_dir, filename), "r").read())
        except:
            print("[INFO] VERSION ALREADY INSTALLED. SKIPPING...")
        
    conn.commit()
    
conn.close()
print("[INFO] DATABASE UPDATED SUCCESSFULLY")