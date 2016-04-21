#!/usr/bin/python
#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from helloworld.items import DetailItem

class weiboSpider(scrapy.Spider):
   name = 'weibo'
   start_urls =  [ 
            "http://weixin.sogou.com/weixin?type=2&query=%B1%B1%BE%A9%B3%B5%D5%B9"
           ]

   #urlregex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
   def parse(self, response):
       #Request details
       links = LinkExtractor(allow=('mp.weixin.qq.com'),
                              restrict_xpaths=('//div[@class="txt-box"]/h4')).extract_links(response)
       for link in links:
           yield Request(link.url, meta={'dont_redirect':True, 'handle_httpstatus_list':[302]},
                         callback=self.parse_detail)
       #Request the next page
       nextPageUrls = items = LinkExtractor(allow=('query'),
                              restrict_xpaths=('//div[@id="pagebar_container"]/a[@id="sogou_next"]')) \
                              .extract_links(response)
       if len(nextPageUrls) > 0:
           yield Request(nextPageUrls[0].url, callback=self.parse)

       
   def parse_detail(self, response):
       title = response.xpath('//title/text()').extract()
       title = title[0].encode('utf8')
       raw = response.body.decode('utf8')
       detail = DetailItem(title=title, url=response.url, raw=raw)
       yield detail

   def parse_redirect(self, response):
       pass
       
        

