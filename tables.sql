#sql lite 3 tables
create table scan_paths (path varchar(500) primary key);

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
);

#alter table files add column width int default 0;
#alter table files add column height int default 0;

#select file_size,md5sum,count(1) from files where ext='.mp4' group by file_size,md5sum having count(1)>1 limit 10;
#select strftime('%Y-%m', create_time) as m, count(1) from files where ext in ('.mp4', '.mov','.avi') group by strftime('%Y-%m', create_time) order by 1;
#insert into scan_paths values('/mnt/备份/李美圣子的 iPhone/');
#insert into scan_paths values('/home/admin/Mobile backup/\“ahfuzhang\”的 iPhone/');
#insert into scan_paths values('/mnt/usbshare2/手机照片备份/');

