import sys,os,os.path
import sqlite3
#from flask import Flask,request
import flask
from all_configs import configs
import datetime

app = flask.Flask(__name__)

@app.route('/video/play')
def play():
    fid = int(flask.request.args.get('fid', '0'))
    tools = ''
    # if fid>0:
    #     tools = '''
    #     <a href="/video/change_w_h?fid=%d">横竖互换</a>
    #     '''%(fid)
    return '''
        <html>
        <head>
        <title>play video:</title>
        <meta charset="utf-8" />
        <style>
        body {padding:0px; margin:0px;}
        img {padding:0px; margin:0px;}
        </style>
        </head>
        <body>
        %s
        <video controls autoplay="1" src="%s" width="100%%" height="100%%"></video>
        </body>
        </html>
        ''' % (tools, flask.request.args.get('v', ''))

@app.route('/video/change_w_h')
def change_w_h():
    fid = int(flask.request.args.get('fid', '0'))
    if fid<=0:
        return 'param error'
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    sql='select full_path,width,height from files where fid=?'
    cursor.execute(sql, (fid,))    
    values = cursor.fetchall()
    if len(values)!=1:
        cursor.close()
        conn.close()
        return 'no fid'
    full_path,w,h = values[0]
    if w>0 and h>0:
        sql='update files where width=?,height=? where fid=?'
        cursor.execute(sql, (h,w,fid,))
        conn.commit()
    cursor.close()
    conn.close()
    

#@app.route('/video/')
# def video1():
#     conn = sqlite3.connect(configs['db'])
#     cursor = conn.cursor()
#     sql='select fid,full_path,create_time from files where ext in (\'.mp4\',\'.mov\',\'.avi\') order by create_time desc limit 100'
#     cursor.execute(sql)
#     values = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     html='''
#         <html>
#         <head>
#         <title> all videos</title>
#         <style>
#         body {padding:0px; margin:0px;}
#         img {padding:0px; margin:0px;}
#         </style>
#         </head>
#         <body style="margin:0px;padding:0px;">
#     '''
#     cnt = 0
#     for row in values:
#         cnt += 1
#         fid,full_path,create_time = row
#         dtm = datetime.datetime.fromisoformat(create_time)
#         new_dir = os.path.join(configs['thumbnail_dir'], dtm.strftime('%Y-%m')+'/')
#         thumbnail = os.path.join(new_dir, 'thumb_%08d.png'%fid)
#         if not os.path.exists(thumbnail):
#             continue
#         html += '''
#             <a href="/video/play?v=/movie/%s/%s_%s" target="_blank"><img src="/movie/thumbnail/%s/thumb_%08d.png"/></a>
#         ''' % (dtm.strftime('%Y-%m'), dtm.strftime('%Y-%m-%d'), os.path.basename(full_path), \
#             dtm.strftime('%Y-%m'), fid)
#         #if cnt%3==0:
#         #    html += '<br/>'
#     #
#     html += '</body></html>'
#     return html

def _write_month_info(cursor, fd):
    sql='select strftime(\'%Y-%m\', create_time) as m, count(1) from files where ext in (\'.mp4\', \'.mov\',\'.avi\') group by strftime(\'%Y-%m\', create_time) order by 1 desc'
    cursor.execute(sql)
    values = cursor.fetchall()
    fd.write('''
    <html>
        <head>
        <meta charset="utf-8" />
        <title> all videos</title>
        <style>
        body {padding:0px; margin:0px;}
        img {padding:0px; margin:0px;}
        </style>
        </head>
        <body>
    ''')
    for row in values:
        month,cnt = row
        fd.write('''
        <a href="/video/month?m=%s">%s</a>(%d) 
        '''%(month, month, cnt)) 
    fd.write('<br/>')

@app.route('/video/month')
def month():
    m = flask.request.args.get('m','')
    
    #
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    #
    sql='select count(1) from files where ext in (\'.mp4\',\'.mov\',\'.avi\') and strftime(\'%Y-%m\', create_time)=?'
    cursor.execute(sql, (m,))
    values = cursor.fetchall()
    cnt = values[0][0]
    start = int(flask.request.args.get('start','0'))
    limit = int(flask.request.args.get('limit','100'))
    if cnt>100:
        month_file=os.path.join(configs['thumbnail_dir'], '%s_%d_%d.html'%(m,start,start+limit))
        page_loc='%s/movie/thumbnail/%s_%d_%d.html'%(configs['host'], m, start,start+limit)
        if os.path.exists(month_file):
            return flask.redirect(page_loc)
        fd_month=open(month_file, 'w')
        _write_month_info(cursor, fd_month)
        pages = cnt//100 if cnt%100==0 else cnt//100+1
        fd_month.write('<hr/>')
        for p in range(pages):
            fd_month.write('''
                <a href="/video/month?m=%s&start=%d&limit=100">%d-%d</a>
            '''%(m, p*100+1, p*100+1, (p+1)*100))
        fd_month.write('<hr/>')
    else:
        month_file=os.path.join(configs['thumbnail_dir'], '%s.html'%m)
        page_loc='%s/movie/thumbnail/%s.html'%(configs['host'], m)
        if os.path.exists(month_file):
            return flask.redirect(page_loc)
        fd_month=open(month_file, 'w')
        _write_month_info(cursor, fd_month)
    #
    sql='select fid,full_path,create_time from files where ext in (\'.mp4\',\'.mov\',\'.avi\') and strftime(\'%Y-%m\', create_time)=? order by create_time desc limit ?,?'
    cursor.execute(sql, (m,start,limit))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    date_str=''
    for row in values:
        fid,full_path,create_time = row
        dtm = datetime.datetime.fromisoformat(create_time)
        dtm_date=dtm.strftime('%Y-%m-%d')
        if dtm_date!=date_str:
            date_str = dtm_date
            fd_month.write('''
            <h1>%s</h1>
            '''%(date_str))
        new_dir = os.path.join(configs['thumbnail_dir'], dtm.strftime('%Y-%m')+'/')
        thumbnail = os.path.join(new_dir, 'thumb_%08d.png'%fid)
        #if not os.path.exists(thumbnail):
        #    continue
        fd_month.write('''
            <a href="/video/play?fid=%d&v=/movie/%s/%s_%s" target="_blank"><img src="/movie/thumbnail/%s/thumb_%08d.png"/></a>
        ''' % (fid, dtm.strftime('%Y-%m'), dtm.strftime('%Y-%m-%d'), os.path.basename(full_path), \
            dtm.strftime('%Y-%m'), fid) )
    #
    fd_month.write('</body></html>')
    fd_month.close()
    return flask.redirect(page_loc)

@app.route('/video/')
def video():
    index_file = os.path.join(configs['thumbnail_dir'], 'index.html')
    if os.path.exists(index_file):
        return flask.redirect('%s/movie/thumbnail/index.html'%(configs['host']))
    conn = sqlite3.connect(configs['db'])
    cursor = conn.cursor()
    fd_index = open(index_file, "w")
    _write_month_info(cursor,fd_index)
    #
    sql='select fid,full_path,create_time from files where ext in (\'.mp4\',\'.mov\',\'.avi\') order by create_time desc limit 100'
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in values:
        fid,full_path,create_time = row
        dtm = datetime.datetime.fromisoformat(create_time)
        new_dir = os.path.join(configs['thumbnail_dir'], dtm.strftime('%Y-%m')+'/')
        thumbnail = os.path.join(new_dir, 'thumb_%08d.png'%fid)
        #if not os.path.exists(thumbnail):
        #    continue
        fd_index.write('''
            <a href="/video/play?fid=%d&v=/movie/%s/%s_%s" target="_blank"><img src="/movie/thumbnail/%s/thumb_%08d.png"/></a>
        ''' % (fid, dtm.strftime('%Y-%m'), dtm.strftime('%Y-%m-%d'), os.path.basename(full_path), \
            dtm.strftime('%Y-%m'), fid) )
    #
    fd_index.write('</body></html>')
    fd_index.close()
    return flask.redirect('%s/movie/thumbnail/index.html'%(configs['host']))

if __name__ == '__main__':
    #app.debug = all_configs['flask_debug']
    default_host = '127.0.0.1'
    argc = len(sys.argv)
    if argc>=2:
        default_host = sys.argv[1]
    default_port = 8080
    if argc>=3:
        default_port = int(sys.argv[2])
    app.run(host=default_host, port=default_port)
'''
this is the end
'''

