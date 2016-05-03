#!/usr/bin/python
#-*-coding:utf-8-*-
import re
import json
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from helloworld.items import DetailItem

class weixinSpider(scrapy.Spider):
   name = 'weixin'
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
       #print response.request.headers
       nextPageUrls = items = LinkExtractor(allow=('query'),
                              restrict_xpaths=('//div[@id="pagebar_container"]/a[@id="sogou_next"]')) \
                              .extract_links(response)
       if len(nextPageUrls) > 0:
           print nextPageUrls[0].text
           yield Request(nextPageUrls[0].url, callback=self.parse)

       
   def parse_detail(self, response):
       title = response.xpath('//title/text()').extract()
       title = title[0].encode('utf8')
       raw = response.body
       detail = DetailItem(title=title, url=response.url, raw=raw, rawcode='utf8')
       #yield detail
       links = re.split(r'\?',response.url)
       readAndlikeUrl =  "%smp/getcomment?%s" % (links[0][:-1], links[1])
       yield Request(readAndlikeUrl, meta={'item':detail}, callback=self.parse_rl)

   def parse_rl(self, response):
       item = response.meta['item']
       res = json.loads(response.body)
       if res['base_resp']['ret']  == 0:
           finaldetail = DetailItem(title=item['title'], url=item['url'], raw=item['raw'], rawcode='utf8',
                                    readnum = res['read_num'], likenum=res['like_num'])
           yield finaldetail
       else:
           yield item
        

