'''
把所有视频都在一个统一目录下建立软链接
'''
import sys,os,os.path
import sqlite3
import datetime

from all_configs import configs

def main():
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    sql='select fid,full_path,create_time from files where ext in (\'.mp4\',\'.mov\',\'.avi\')'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in values:
        fid,full_path,create_time = row
        dtm = datetime.datetime.fromisoformat(create_time)
        new_dir = configs['target_dir'] + \
            dtm.strftime('%Y-%m') + '/'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_link = os.path.join(new_dir, dtm.strftime('%Y-%m-%d_')+os.path.basename(full_path))
        if not os.path.exists(new_link):
            cmd = 'ln -s \"%s\" \"%s\"'%(full_path, new_link)
            os.system(cmd)
            print(cmd)

if __name__=='__main__':
    main()
