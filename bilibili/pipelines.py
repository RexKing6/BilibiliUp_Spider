# -*- coding: utf-8 -*-

import json
import codecs
import logging


class BilibiliJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('biliup.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()


import MySQLdb
import mysql.connector as conner
from bilibili.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DBNAME, MYSQL_POOLNAME, MYSQL_POOLSIZE


class BilibiliMysqlPipeline(object):
	def __init__(self):
		self.conn = conner.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME, pool_name=MYSQL_POOLNAME, pool_size=MYSQL_POOLSIZE)
		self.cursor = self.conn.cursor()
		self.cursor.execute('SET character_set_server=utf8;')
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')
	
	def process_item(self, item, spider):
		uid = item['uid']
		self.cursor.execute('select * from biliup where uid=%s' % (uid))
		if self.cursor.fetchone():
			sql = "update biliup set name='%s', space='%s', sex='%s', birthday='%s', address='%s', level='%s', regtime='%s', fans=%s, follows=%s, playnum=%s, videonum=%s, videocate='{json}' where uid=%s" % (item['name'],item['space'],item['sex'],item['birthday'],item['address'],item['level'],item['regtime'],item['fans'],item['follows'],item['playnum'],item['videonum'],item['uid'])
		else:
			if item['regtime']:
				sql = "insert into biliup values(%s,'%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'{json}')" % (item['uid'],item['name'],item['space'],item['sex'],item['birthday'],item['address'],item['level'],item['regtime'],item['fans'],item['follows'],item['playnum'],item['videonum'])
			else:
				sql = "insert into biliup(uid,name,space,sex,birthday,address,level,fans,follows,playnum,videonum,videocate) values(%s,'%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'{json}')" % (item['uid'],item['name'],item['space'],item['sex'],item['birthday'],item['address'],item['level'],item['fans'],item['follows'],item['playnum'],item['videonum'])
		s = json.dumps(item['videocate'])
		sql = sql.format(json=MySQLdb.escape_string(s))
		self.cursor.execute(sql)
		self.conn.commit()
		return item
		