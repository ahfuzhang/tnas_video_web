#!/bin/python
import sys,os,os.path
import subprocess
import json
import re
import datetime

g_dtm_format=re.compile(r'(\d{4})-(\d{2})-(\d{2})\D+(\d{2}):(\d{2}):(\d{2})')
g_w_h_format=re.compile(r'width=(\d+)\D+height=(\d+)')

def ffprobe_get_width_height(full_path):
    if not os.path.exists(full_path):
        return False,0,0
    cmd = 'ffprobe "%s"'%full_path
    #print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out_str = p.communicate('')
    #print('out_str:', out_str)
    arr=g_w_h_format.split(out_str[0].decode('utf-8'))
    if len(arr)>=3:
        return True,int(arr[1]),int(arr[2])
    return False,0,0

def ffprobe_get_json(full_path):
    if not os.path.exists(full_path):
        return False,None
    cmd = 'ffprobe -v error -show_format "%s" -of json | sed "2,5d"'%full_path
    #print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #print('out_str:', out_str)
    out_str = p.communicate('')
    #print('out_str:', out_str)
    try:
        j = json.loads(out_str[0])
    except:
        return False,None
    return True,j

def ffprobe_get_create_date_duration(full_path):
    ret,j = ffprobe_get_json(full_path)
    if not ret:
        return False,None,0.0
    if 'format' not in j:
        return False,None,0.0
    fmt = j['format']
    duration = float(fmt.get('duration', '0.0'))
    if 'tags' not in fmt:
        return True,None,duration
    tags = fmt['tags']
    if 'date' in tags:
        arr = g_dtm_format.split(tags['date'])
        if len(arr)<7:
            return True,None,duration
        dtm = datetime.datetime.fromisoformat('%s-%s-%s %s:%s:%s'%\
            (arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]))
        return True, dtm, duration        
    if 'creation_time' not in tags:
        return True,None,duration
    arr = g_dtm_format.split(tags['creation_time'])
    if len(arr)<7:
        return True,None,duration
    dtm = datetime.datetime.fromisoformat('%s-%s-%s %s:%s:%s'%\
        (arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]))
    return True, dtm, duration

if __name__=='__main__':
    argc = len(sys.argv)
    if argc<2:
        print('usage:%s <mp4>'%sys.argv[0])
        sys.exit()
    ret,j = ffprobe_get_json(sys.argv[1])
    if not ret:
        print('fail')
        sys.exit()
    #print(j)
    print('json:',j)
    print('create date and duration:', ffprobe_get_create_date_duration(sys.argv[1]))
    #
    print('width and height:', ffprobe_get_width_height(sys.argv[1]))

#python ffprobe_tools.py /mnt/public/微云网盘/12304685/家庭视频/2015年09月/IMG_0530.MOV
#     