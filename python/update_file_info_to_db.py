#!/bin/python
# 扫描文件，写入sqlite

import sys,os,os.path
import datetime
import sqlite3
import json
from public_lib.ffprobe_tools import *
from public_lib.md5sum4file import md5sum
from public_lib.jpeg_tools import jpeg_get_read_datetime
from all_configs import configs

def each_file(f, conn, cursor):
    try:
        s = os.stat(f)
        if s.st_size==0:
            os.remove(f)
            return
    except Exception as err:
        print('    stat fail:', err)
        return
    sql = 'insert into files(full_path,ext,create_time,file_size) values(?,?,?,?)'
    _, file_extension = os.path.splitext(f)
    file_extension = file_extension.lower()
    if 'file_type_filter' in configs and len(configs['file_type_filter'])>0:
        if file_extension not in configs['file_type_filter']:
            return
    create_dtm = datetime.datetime.fromtimestamp(s.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    fid = 0
    md5_size = 1024*1024*10 if s.st_size>1024*1024*10 else s.st_size
    try:
        cursor.execute(sql, (f, file_extension.lower(), create_dtm, s.st_size))
        fid = cursor.lastrowid
        md5_str = md5sum(f, md5_size).hex()
        duration = 0.0
    except:
        print('    already exists')
        sql = 'select fid,create_time,duration,md5sum from files where full_path=?'
        cursor.execute(sql, (f,))
        values = cursor.fetchall()
        if len(values)!=1:
            return
        fid,create_dtm,duration,md5_str = values[0]
        if md5_str!='':
            return
    print('    fid:',fid)
    #
    if file_extension in ['.jpg', '.jpeg', '.png']:
        ret,dtm = jpeg_get_read_datetime(f)
        if ret:
            create_dtm = dtm.strftime('%Y-%m-%d %H:%M:%S')
    if file_extension in ['.mp4', '.mov']:
        ret,dtm,d = ffprobe_get_create_date_duration(f)
        if ret:
            if dtm is not None:
                create_dtm = dtm
            duration = d        
        # ret,j = ffprobe_get_json(f)
        # if ret:
        #     if 'date' not in j['format'] and 'creation_time' not in j['format']['tags']:
        #         print(j)
        #         #sys.exit()
        #     if 'date' in j['format']:
        #         create_dtm = datetime.datetime.fromisoformat(j['format'].get('date', '')).strftime('%Y-%m-%d %H:%M:%S')
        #     elif 'creation_time' in j['format']:
        #         create_dtm = datetime.datetime.fromisoformat(j['format']['tags'].get('creation_time', '')).strftime('%Y-%m-%d %H:%M:%S')
        #     duration = float(j['format']['duration'])
    #
    sql = 'update files set create_time=?,duration=?,md5sum=? where fid=?'
    cursor.execute(sql, (create_dtm,duration,md5_str,fid))
    #conn.commit()
    #print(dir(cursor), repr(cursor))

def each_folder(folder, conn, cursor):
    for parent,folders,files in os.walk(folder):
        if len(folders)==0 and len(files)==0:
            os.removedirs(parent)
            continue
        for f in files:
            print('%s'%os.path.join(parent, f))
            each_file(os.path.join(parent, f), conn, cursor)
        #return    
        conn.commit()

def init():
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    cursor.execute('''
    create table scan_paths (path varchar(500) primary key)
    ''')
    cursor.execute('''
        create table files(
        fid integer primary key autoincrement,
        full_path varchar(600) unique,
        ext varchar(10),
        create_time datetime,
        file_size bigint,
        duration double,
        md5sum varchar(32),
        width int default 0,
        height int default 0
        )
    ''')
    conn.commit()

    if 'src_dirs' not in configs or len(configs['src_dirs'])==0:
        print('no src dir')
        sys.exit(-1)
    for item in configs['src_dirs']:
        cursor.execute("insert into scan_paths values(?)", (item,))  
    conn.commit()
    #
    cursor.close()
    conn.close()

def main():
    if not os.path.exists(configs['db']):
        init()
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    cursor.execute('select path from scan_paths')
    values = cursor.fetchall()
    for row in values:
        each_folder(row[0], conn, cursor)
    cursor.close()
    conn.close()
    print('complete')

if __name__=='__main__':
    main()




