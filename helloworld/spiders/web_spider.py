#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
import re, json
from pyquery import PyQuery as pq
from lxml.html import tostring
import codecs

class WebWeiboSpider(scrapy.Spider):
   name = 'webweibo'
   start_urls = [ "http://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E8%25BD%25A6%25E5%25B1%2595&Refer=index"
           ]


   def parse(self, response):
        #print response.body
        print 'start parse===='
        jQuery = pq(response.body)
        scripts = jQuery('script')
        text = "".join(filter(lambda x: x is not None, [x.text for x in scripts]))
       
        #with codecs.open('rawdata2','wb', 'utf8') as f:
        #    f.write(unicode(text))
        #print text
        card_match = re.search(r'{(\"pid\":\"pl_common_searchTop\".*)}', unicode(text), re.M|re.I)
        if card_match:
            print 'got it'
        #for script in scripts:
        #    match = re.search(r'{(\"pid\":\"pl_weibo_feedlist\".*)}', unicode(script.text), re.M | re.I)
        #    if match:
        #        search_results = pq(json.loads(match.group())['html'])
        #        feeds = search_results('dl.feed_list')
        #        for feed in feeds:
        #            print tostring(feed)
        print 'parse finish======'

