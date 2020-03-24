#!/bin/python
# 从SQL lite中删除重复文件

import sys,os,os.path
import datetime
import sqlite3
import json
from public_lib.ffprobe_tools import ffprobe_get_json
from public_lib.md5sum4file import md5sum
from public_lib.jpeg_tools import jpeg_get_read_datetime

from all_configs import configs

def remove_dup_files(file_size,md5_str,conn,cursor):
    sql = 'select fid,full_path,create_time from files where file_size=? and md5sum=? order by create_time ASC'
    cursor.execute(sql, (file_size,md5_str,))
    values = cursor.fetchall()
    if len(values)<2:
        return
    dict_fid = {}
    #dict_dtm = {}
    min_len = 100000
    selected_fid = -1
    for row in values:
        fid,full_path,create_time = row
        arr = full_path.split('/')
        if len(arr)<min_len:   #保留存储深度最短的文件
            min_len = len(arr)
            selected_fid = fid
        dict_fid[fid] = [full_path,create_time]
        #timestamp = datetime.datetime.fromisoformat(create_time).timestamp()
        #dict_dtm[timestamp] = fid
        #print(create_time, type(create_time), repr(create_time))
    if selected_fid==-1:
        assert False
    for k in dict_fid:
        if k==selected_fid:
            continue
        full_path,create_time = dict_fid[k]
        # if full_path.startswith('/mnt/public/'):
        #     target_dir = os.path.join(TARGET_PATH, '.'+os.path.dirname(full_path))
        #     if not os.path.exists(target_dir):
        #         os.makedirs(target_dir)
        #     target_file = os.path.join(TARGET_PATH, '.'+full_path)
        #     if os.path.exists(full_path):
        #         os.rename(full_path, target_file)
        #     print('move:', full_path)
        # else:
        #     os.remove(full_path)
        #     print('delete:', full_path)
        target_dir = os.path.join(configs['move_dup_files_to'], '.'+os.path.dirname(full_path))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target_file = os.path.join(configs['move_dup_files_to'], '.'+full_path)
        if os.path.exists(full_path):
            #os.rename(full_path, target_file)
            cmd = 'mv "%s" "%s"'%(full_path, target_file)
            os.system(cmd)
        print('move:', full_path)        
        #sql
        sql='delete from files where fid=?'
        cursor.execute(sql, (k,))
    #
    conn.commit()

def main():
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    sql = 'select file_size,md5sum,count(1) from files group by file_size,md5sum having count(1)>1 limit 100'
    while True:
        cursor.execute(sql)
        values = cursor.fetchall()
        if len(values)==0:
            print('complete')
            break
        for row in values:
            file_size,md5_str,_ = row
            remove_dup_files(file_size,md5_str,conn,cursor)
            #return
            #each_folder(row[0], conn, cursor)
        #break
    cursor.close()
    conn.close()

if __name__=='__main__':
    main()
