import sys, os, os.path
import datetime
import re
from exif import Image

datetime_format=re.compile(r'(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})')

def jpeg_get_read_datetime(full_path):
    '''
    从JPEG文件的tag中获得真正的创建日期
    '''
    if not os.path.exists(full_path):
        return False, None
    f = open(full_path, 'rb')
    try:
        my_img = Image(f)
        datetime_str = my_img.datetime
    except:
        return False,None
    f.close()
    arr = datetime_format.split(datetime_str)
    if len(arr)<7:
        return False,None
    try:
        return True, datetime.datetime.fromisoformat('%s-%s-%s %s:%s:%s'%\
        (arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]))
    except:
        return False,None
        
if __name__=='__main__':
    argc = len(sys.argv)
    if argc<2:
        print("usage:%s <jpeg>"%sys.argv[0])
        sys.exit()
    ret,dtm = jpeg_get_read_datetime(sys.argv[1])
    if not ret:
        print("fail")
        sys.exit()
    print('ok:', dtm)

# python jpeg_tools.py /mnt/public/微云网盘/12304685/照片/2017-12_圣子_iphone6sp/2017年1月9日/IMG_0258.JPG
#     