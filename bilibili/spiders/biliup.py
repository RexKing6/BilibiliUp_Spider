import copy
import json
import time
import scrapy
import logging
from scrapy import Request
from scrapy import FormRequest
from bilibili.items import BilibiliItem
from scrapy_redis.spiders import RedisSpider
import sys
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Rexking'

class BiliupSpider(RedisSpider):
	name = 'biliup'
	redis_key = 'biliup:start_urls'

	def parse(self, response):
		headers = {'Referer': 'http://space.bilibili.com/1'}
		url = 'https://space.bilibili.com/ajax/member/GetInfo'
		mid = response.url.split('/')[-1]
		data = {'mid': mid}
		yield FormRequest(url, callback=self.parse_up, headers=headers, formdata=data)

	def parse_up(self, response):
		user = json.loads(response.text)
		if not user['status']:
			return
		user = user['data']
		item = BilibiliItem()
		item['uid'] = user['mid']
		item['name'] = user['name']
		item['space'] = 'https://space.bilibili.com/' + item['uid']
		item['sex'] = user['sex']
		try:
			item['birthday'] = user['birthday'][-5:]
		except KeyError:
			item['birthday'] = ''
		try:
			item['address'] = user['place']
		except KeyError:
			item['address'] = ''
		item['level'] = user['level_info']['current_level']
		try:
			t = time.localtime(user['regtime'])
			item['regtime'] = time.strftime('%Y-%m-%d',t)
		except KeyError:
			item['regtime'] = ''
		item['fans'] = user['fans']
		item['follows'] = user['attention']
		item['playnum'] = user['playNum']

		url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + item['uid']
		yield Request(url, callback=self.parse_video, meta={'userdata': item})

	def parse_video(self, response):
		item = response.meta['userdata']
		data = json.loads(response.text)
		if not data['status']:
			return
		data = data['data']
		item['videonum'] = data['count']
		if data['tlist']:
			videocate = {}
			for i in data['tlist']:
				videocate[data['tlist'][i]['name']] = data['tlist'][i]['count']
			item['videocate'] = videocate
		else:
			item['videocate'] = ''
		yield item

'''
class BiliupSpider(scrapy.Spider):
	name = 'biliup'

	def start_requests(self):
		headers = {'Referer': 'http://space.bilibili.com/1'}
		url = 'https://space.bilibili.com/ajax/member/GetInfo'
		for mid in range(1, 17000000):
			data = {'mid': str(mid)}
			logging.info(mid)
			yield FormRequest(url, callback=self.parse_up, headers=headers, formdata=data)

	def parse_up(self, response):
		user = json.loads(response.text)
		if not user['status']:
			return
		user = user['data']
		item = BilibiliItem()
		item['uid'] = user['mid']
		item['name'] = user['name']
		item['space'] = 'https://space.bilibili.com/' + item['uid']
		item['sex'] = user['sex']
		try:
			item['birthday'] = user['birthday'][-5:]
		except KeyError:
			item['birthday'] = ''
		try:
			item['address'] = user['place']
		except KeyError:
			item['address'] = ''
		item['level'] = user['level_info']['current_level']
		try:
			t = time.localtime(user['regtime'])
			item['regtime'] = time.strftime('%Y-%m-%d',t)
		except KeyError:
			item['regtime'] = ''
		item['fans'] = user['fans']
		item['follows'] = user['attention']
		item['playnum'] = user['playNum']

		url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + item['uid']
		yield Request(url, callback=self.parse_video, meta={'userdata': item})

	def parse_video(self, response):
		item = response.meta['userdata']
		data = json.loads(response.text)
		if not data['status']:
			return
		data = data['data']
		item['videonum'] = data['count']
		if data['tlist']:
			videocate = {}
			for i in data['tlist']:
				videocate[data['tlist'][i]['name']] = data['tlist'][i]['count']
			item['videocate'] = videocate
		else:
			item['videocate'] = ''
		yield item
'''