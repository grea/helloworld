# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarShowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()

class WeiboItem(scrapy.Item):
    url = scrapy.Field()
    raw = scrapy.Field()

class DetailItem(scrapy.Item):    
    title = scrapy.Field()
    raw = scrapy.Field()
    rawcode = scrapy.Field()
    url = scrapy.Field()
    readnum = scrapy.Field()
    likenum = scrapy.Field()
class youkuItem(scrapy.Item):
    media = scrapy.Field()
