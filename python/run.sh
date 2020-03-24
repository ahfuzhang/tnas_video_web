python update_file_info_to_db.py
python remove_dup_files.py >> log.txt
python make_video_cover.py >> log.txt
python make_link.py >> log.txt
nohup python video_server.py 127.0.0.1 8081 &> /dev/null &

