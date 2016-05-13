# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from helloworld.items import youkuItem

class YoukuSpider(scrapy.Spider):
    name = "youku"
    allowed_domains = ["youku.com"]
    start_urls = (
            'http://www.youku.com/v_olist/c_97_s_6_d_1.html',
    )
    setnum_pattern = re.compile(r'(\d)+')

    def parse(self, response):
        tvs = response.xpath('//div[@class="yk-col3"]')
        for tv in tvs:
            url = tv.xpath('.//a/@href').extract()
            title = tv.xpath('.//a/text()').extract()
            last_update = tv.xpath('.//span[@class="p-num"]/text()').extract()[0]
            last_update = ''.join(last_update.split())
            set_num_s = tv.xpath('.//span[@class="p-status"]/text()').extract()
            if set_num_s and len(set_num_s) > 0:
                match = self.setnum_pattern.search(set_num_s[0])
                if match:
                    setnum = int(match.group())
                    print "%s---%s===%s" % (title[0], setnum,last_update)
            #yield Request(url[0], callback=self.parse_tv)
        next_page = response.xpath('//li[@class="next"]/a/@href').extract()
        if next_page:
            next_page_url = 'http://www.youku.com' + next_page[0]
            #print next_page_url            
            yield Request(next_page_url, callback=self.parse)

    def parse_tv(self, response):
        pass
