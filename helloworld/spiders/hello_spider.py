#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
import re, json
from pyquery import PyQuery as pq
from lxml.html import tostring
import codecs
from helloworld.items import WeiboItem

class helloSpider(scrapy.Spider):
   name = 'hello'
   start_urls = [ "http://s.weibo.com/weibo/%25E5%258C%2597%25E4%25BA%25AC%25E8%25BD%25A6%25E5%25B1%2595&Refer=index"
           #"http://m.weibo.cn/main/pages/index?containerid=100103type%3D1%26q%3D%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95&type=all&queryVal=%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95&luicode=20000174&title=%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95"
           ]


   def parse(self, response):
        #print response.body
        print 'start parse===='
        jQuery = pq(response.body)
        scripts = jQuery('script')
        text = "".join(filter(lambda x: x is not None, [x.text for x in scripts]))
        #print text
        weibomatch = re.search(r'{(\"pid\":\"pl_weibo_direct\".*?)}', text, re.M|re.I)
                              #r'{(\"pid\":\"pl_common_totalshow\".*?)}
        if weibomatch:
            print "*************"
            html = json.loads(weibomatch.group())['html']
            #Save weibo HTML
            weiboitem = WeiboItem(raw= html)
            #with codecs.open ('weibo.html', 'wb', 'utf8') as f:               
            #    f.write(html)
            #print html
            return weiboitem
        #weibomatch = re.search(r'{(\'stage\')}', text, re.M|re.I)
        #if card_match:
        #    print 'got it'
        #    #print card_match.group(1)
        #    html = json.loads(card_match.group(1))
        #    print html
        #if match:
        #    print 'xxxxxxxxxxx'
        #    print match.group(0)
        #selector = Selector(response)
        #tweets = selector.xpath('body/div[@class="card" and @id]')
        #n = 1
        
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

