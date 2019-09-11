# -*- coding: utf-8 -*-

import pymysql
from comicscrapy.settings import MYSQL_HOST
from comicscrapy.settings import MYSQL_PORT
from comicscrapy.settings import MYSQL_DBNAME
from comicscrapy.settings import MYSQL_USER
from comicscrapy.settings import MYSQL_PASSWD
import datetime

class ComicscrapyPipeline(object):
    def __init__(self):
        host =MYSQL_HOST
        port = MYSQL_PORT
        dbname = MYSQL_DBNAME
        user = MYSQL_USER
        passwd = MYSQL_PASSWD
        print(host,port,dbname,user,passwd)
        self.db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=dbname, charset='utf8')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        sql='''
INSERT INTO comic (author,name,intr,cover,comic_url,comic_type,comic_type2,collection,recommend,praise,roast,last_update_chapter,last_update_time,status,add_time) 
VALUES ('%(author)s','%(name)s','%(intr)s','%(cover)s','%(comic_url)s','%(comic_type)s','%(comic_type2)s',%(collection)d,%(recommend)d,%(praise)d,%(roast)d,'%(last_update_chapter)s','%(last_update_time)s',%(status)d,'%(add_time)s') 
ON DUPLICATE KEY UPDATE author='%(author)s',name='%(name)s',intr='%(intr)s',cover='%(cover)s',comic_url='%(comic_url)s',
comic_type='%(comic_type)s',comic_type2='%(comic_type2)s',collection=%(collection)d,recommend=%(recommend)d,praise=%(praise)d,
roast=%(roast)d,last_update_chapter='%(last_update_chapter)s',last_update_time='%(last_update_time)s',status=%(status)d
'''
        now = datetime.datetime.now()  ##now为datetime（即时间类型）
        timestr = now.strftime("%Y-%m-%d %H:%M:%S")
        item['add_time']=timestr
        sql = sql % dict(item)
        try:
            self.cur.execute(sql)
            self.db.commit()
            return item
        except:
            print('mysql insert exception:'+sql)

    def close_spider(self,spider):
        self.db.close()

# class TestPipeline(object):
#     def process_item(self, item, spider):
#         print 'hellow'
#         return item
