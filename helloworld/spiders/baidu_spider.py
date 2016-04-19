#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import re, json
from pyquery import PyQuery as pq
from lxml.html import tostring
import codecs
from helloworld.items import CarShowItem
from helloworld.items import DetailItem

class baiduSpider(scrapy.Spider):
   name = 'baidu'
   start_urls =  [
           "https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E8%BD%A6%E5%B1%95&rsv_spt=1&rsv_iqid=0xd621d4b20000e9f0&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=10&rsv_sug1=9&rsv_sug7=100&rsv_sug2=0&inputT=25288&rsv_sug4=25289"
           #"https://www.baidu.com/s?wd=scrapy%20shell%E8%AE%BE%E7%BD%AEuser%20agent&pn=60&oq=scrapy%20shell%E8%AE%BE%E7%BD%AEuser%20agent&ie=utf-8&rsv_pq=b0aa184900183467&rsv_t=d56cOy5hF0aPnkSY3C%2BX9VIY57sy3fVMXpgr%2Bm0l63vhYqhzhHH0odL%2BBGw"
           ]

   def parse(self, response):
       #print response.body
       #with open("baidu.html", 'wb') as f:
       #    f.write(response.body)
       n = 1
       cars = []
       content_divs = response.xpath("//div[@id='content_left']/div[@id]")
                  #sites = sel.xpath("//div[@id='content_left']/div[@id]")
       for div in content_divs:
           print "==========item %s========" % n
           n = n + 1
           #print div.xpath('.//h3/a/text()').extract()
           title = div.xpath('.//h3/a/text()').extract()
           #print div.xpath('.//h3/a/@href').extract()
           url = div.xpath('.//h3/a/@href').extract()
           #print div.xpath('.//div[@class="c-abstract"]/text()').extract()
           desc = div.xpath('.//div[@class="c-abstract"]/text()').extract()
           if len(url) == 0:
               continue
           car = CarShowItem(title = title, description = desc, url = url)           
           yield car
           yield Request("".join(url), meta={'item': car, 'dont_redirect': True,
                        'handle_httpstatus_list':[302]},
                         callback=self.parse_detail, )
           #cars.append(car)
       #return cars
       pages = response.xpath("//div[@id='page']/a")
       #print "pages %d " % len(pages)
       pageindex = 1
       for page in pages:
           if len(page.xpath('text()').extract()) == 0:
               print 'index page'
           else:
               print 'next page'
               #print page.xpath('text()').extract()
               #print page.xpath('@href').extract()
               if pageindex > 1:
                   nexturl = "http://www.baidu.com" + "".join(page.xpath('@href').extract())
                   print nexturl
                   yield Request(nexturl, callback=self.parse)
                   break
           pageindex = pageindex + 1


   def parse_detail(self, response):
        redirection_url = response.headers.get('location')
        car = response.meta['item']
        if redirection_url == None:
            detail = DetailItem(title=car['title'], url=car['url'], raw=response.body)
            #print detail
            yield detail
        else:
            yield Request(redirection_url, meta={'item': car},callback=self.parse_redirect)

   def parse_redirect(self, response):
       car = response.meta['item']
       detail = DetailItem(title=car['title'], url=car['url'], raw=response.body)
       yield detail
        

