#!/bin/python
import sys,os,os.path
import subprocess
#import json
#import re
#import datetime
from ffprobe_tools import *

def video_get_cover(mp4, target):
    cmd='ffmpeg -i "%s" -ss 00:00:1 -vframes 1 -hide_banner -loglevel panic "%s"'%\
        (mp4, target)
    subprocess.call(cmd, shell=True)
    return os.path.exists(target)

def video_set_size(mp4, target, width, height):
    cmd='ffmpeg -i "%s" -hide_banner -loglevel panic -s %dx%d "%s"'%\
        (mp4, width, height, target)
    subprocess.call(cmd, shell=True)
    return os.path.exists(target)

def video_change_width_to_height(mp4):
    ret,w,h = ffprobe_get_width_height(mp4)
    if not ret:
        return False,'ffprobe_get_width_height fail'
    os.rename(mp4, mp4+'.old')
    ret = video_set_size(mp4+'.old', mp4, h, w)
    if not ret:
        return False,'video_set_size fail'
    os.remove(mp4+'.old')
    return True,'success'

if __name__=='__main__':
    argc = len(sys.argv)
    if argc<3:
        print('usage:%s <cmd> <mp4> [other]'%sys.argv[0])
        sys.exit()
    cmd=sys.argv[1]
    if cmd=='get_cover' and argc>=4:
        print(video_get_cover(sys.argv[2], sys.argv[3]))
    elif cmd=='change_w_h':
        print(video_change_width_to_height(sys.argv[2]))
    else:
        print('not support:', cmd)