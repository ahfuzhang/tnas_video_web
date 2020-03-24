#生成视频的封面图
import sys,os,os.path
from PIL import Image,ImageDraw
import sqlite3
import datetime
from public_lib.ffmpeg_tools import video_get_cover

from all_configs import configs

# configs={
#     'db':'/mnt/appdata/temp/test.db',
#     'target_dir':'/mnt/public/movie/',
#     'thumbnail_dir':'/mnt/public/movie/thumbnail/',
#     'thumbnail_size':360
# }

def image_get_thumb(f, size, target):
    img = Image.open(f)
    w,h = img.size
    if w>h:
        img1 = img.crop(((w-h)//2,0, w-(w-h)//2, h-1))
    elif h>w:
        img1 = img.crop((0, (h-w)//2, w-1, h-(h-w)//2))
    else:
        img1 = img
    img2 = img1.resize((size, size))
    img2.save(target)
    return True,w,h

def image_get_thumb_and_text(f, size, target, dtm, duration):
    img = Image.open(f)
    w,h = img.size
    if w>h:
        img1 = img.crop(((w-h)//2,0, w-(w-h)//2, h-1))
    elif h>w:
        img1 = img.crop((0, (h-w)//2, w-1, h-(h-w)//2))
    else:
        img1 = img
    img2 = img1.resize((size, size))
    d = ImageDraw.Draw(img2)
    d.text((10, 355-30), '%.1fS'%round(duration,1))
    d.text((10, 355-20), '%dX%d'%(w,h))
    d.text((10, 355-10), dtm.strftime('%Y-%m-%d %H:%M'))
    img2.save(target)
    return True,w,h

def main():
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    sql='select fid,full_path,create_time,duration,width,height from files where ext in (\'.mp4\',\'.mov\',\'.avi\')'
    cursor.execute(sql)
    values = cursor.fetchall()
    #cursor.close()
    #conn.close()
    for row in values:
        fid,full_path,create_time,duration,width,height = row
        dtm = datetime.datetime.fromisoformat(create_time)
        new_dir = os.path.join(configs['thumbnail_dir'], dtm.strftime('%Y-%m')+'/')
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        cover = os.path.join(new_dir, 'cover_%08d.png'%fid)
        if not os.path.exists(cover):
            print('make cover:', full_path, cover)
            video_get_cover(full_path, cover)
        thumbnail = os.path.join(new_dir, 'thumb_%08d.png'%fid)
        #if os.path.exists(cover) and not os.path.exists(thumbnail):
        if os.path.exists(cover):
            if not os.path.exists(thumbnail):
                print('make thumb:', thumbnail)
                _,w,h = image_get_thumb_and_text(cover, configs['thumbnail_size'], thumbnail, \
                    dtm, duration)
            else:
                w = width
                h = height
            #_,w,h = image_get_thumb(cover, configs['thumbnail_size'], thumbnail)
            #
            if width==0 or height==0:
                sql='update files set width=?,height=? where fid=?'
                cursor.execute(sql, (w,h,fid))
                conn.commit()
    #
    cursor.close()
    conn.close()

if __name__=='__main__':
    main()