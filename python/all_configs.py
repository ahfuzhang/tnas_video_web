import sys

configs = {
    'db':'./20200320_1.db',  #SQLITE文件所在的目录
    'target_dir':'/mnt/public/movie/',  #静态文件的目录
    'thumbnail_dir':'/mnt/public/movie/thumbnail/',  #缩略图的目录
    'thumbnail_size':360,   #缩略图的大小
    'host':'http://192.168.31.3:8080',  #铁威马的WEB服务的访问地址
    #
    'move_dup_files_to':'/mnt/public/dup_files_20200320/', #把重复的文件移动到这个目录
    'src_dirs':[  #需要在哪些目录下扫描文件
        '/mnt/备份/work_disk/',
        '/mnt/admin/Mobile backup/“ahfuzhang”的 iPhone/',
        '/mnt/备份/cepheus/'
    ],
    'file_type_filter':['.mp4', '.mov', '.avi'],  #过滤的文件类型，如果不填，就对所有的文件去重
}
