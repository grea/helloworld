#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
import re, json
from pyquery import PyQuery as pq
from lxml.html import tostring
import codecs

class helloSpider(scrapy.Spider):
   name = 'hello'
   start_urls = [ #"http://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E8%25BD%25A6%25E5%25B1%2595&Refer=index"
           "http://m.weibo.cn/main/pages/index?containerid=100103type%3D1%26q%3D%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95&type=all&queryVal=%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95&luicode=20000174&title=%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95"
           ]


   def parse(self, response):
        #print response.body
        print 'start parse===='
        jQuery = pq(response.body)
        scripts = jQuery('script')
        text = "".join(filter(lambda x: x is not None, [x.text for x in scripts]))
        card_match = re.search(r'{(\"card_type\":\"9\".*)}', unicode(text), re.M|re.I)
        #weibomatch = re.search(r'{(\'stage\')}', text, re.M|re.I)
        if card_match:
            print 'got it'
            #print card_match.group(1)
            html = json.loads(card_match.group(1))
            print html
        #if match:
        #    print 'xxxxxxxxxxx'
        #    print match.group(0)
        #selector = Selector(response)
        #tweets = selector.xpath('body/div[@class="card" and @id]')
        #n = 1
        #for tweet in tweets:
        #    print n
        #    n = n+1
        #    #tweetsItems = TweetsItem()
        #    id = tweet.xpath('@id').extract_first()  # 微博ID
        #    content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
        #    cooridinates = tweet.xpath('div/a/@href').extract_first()  # 定位坐标
        #    like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
        #    transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
        #    comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
        #    others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台

        #    print '=================='
        #    print id
        #    print content
        #    print comment

        
        #with open('rawdata1','wb') as f:
        #    f.write(response.body)
        #print text
        #for script in scripts:
        #    match = re.search(r'{(\"pid\":\"pl_weibo_feedlist\".*)}', unicode(script.text), re.M | re.I)
        #    if match:
        #        search_results = pq(json.loads(match.group())['html'])
        #        feeds = search_results('dl.feed_list')
        #        for feed in feeds:
        #            print tostring(feed)
        print 'parse finish======'

