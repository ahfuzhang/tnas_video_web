#!/bin/python

import sys,os,os.path
import datetime
import sqlite3

TARGET_PATH='/mnt/public/dup_files/'

def each_file(f, conn, cursor):
    _, file_extension = os.path.splitext(f)
    file_extension = file_extension.lower()
    if file_extension not in ['.mp4', '.mov']:
        return
    base_name=os.path.basename(f)
    dir_name=os.path.dirname(f)
    if not base_name.startswith('fast_start_'):
        return
    old=os.path.join(dir_name, base_name[11:])
    if not os.path.exists(old):
        return
    new_path = os.path.join(TARGET_PATH, '.'+old)
    if not os.path.exists(os.path.dirname(new_path)):
        os.makedirs(os.path.dirname(new_path))
    os.rename(old, new_path)
    #
    sql='delete from files where full_path=?'
    cursor.execute(sql, (old,))
    conn.commit()

def main(p):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    for parent,_,files in os.walk(p):
        for f in files:
            each_file(os.path.join(parent, f), conn, cursor)
            #print('%s'%os.path.join(parent, f))

if __name__=='__main__':
    if len(sys.argv)<2:
        print('usage:%s <folder>'%sys.argv[0] )
        sys.exit()
    main(sys.argv[1])    