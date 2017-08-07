# -*- coding: utf-8 -*-
import scrapy

class BilibiliItem(scrapy.Item):
    uid = scrapy.Field()
    name = scrapy.Field()
    space =scrapy.Field()
    sex = scrapy.Field()
    birthday = scrapy.Field()
    address = scrapy.Field()
    level = scrapy.Field()
    regtime = scrapy.Field()
    fans = scrapy.Field()
    follows = scrapy.Field()
    playnum = scrapy.Field()
    videonum = scrapy.Field()
    videocate = scrapy.Field()