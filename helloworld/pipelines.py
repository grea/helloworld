# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import codecs
import re, json
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
  
from hbase import Hbase
from hbase.ttypes import *
from helloworld.thriftool import hbaseutil

class HelloworldPipeline(object):
    """
    def __init__(self):
       self.file = codecs.open('cars_data.json',mode='wb',encoding='utf-8')

    def process_item(self, item, spider):
       line = json.dumps(dict(item)) + '\n'
       self.file.write(line)
    """
    def __init__(self):
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)  
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = Hbase.Client(protocol)
        transport.open()

    def process_item(self, item, spider):
       title = item['title'].decode('utf8')
       url = item['url'].decode('utf8')
       rawcode = item['rawcode']
       #decode the raw content to unicode with right code
       raw = item['raw'].decode(rawcode, errors='ignore')
       #print title
       #print url
       #print raw
       hbaseutil.insertRow(self.client, "baiduweibo", title, url, raw)
       return item


