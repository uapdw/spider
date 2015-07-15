from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import datetime
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class YosSpider(CrawlSpider):
	name = 'yos'
	allowed_domains = ['yos.com.cn']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news
	start_urls = ['http://www.yos.com.cn/xwzx/qydt/']

        def __init__(self,**kw):
          self.host = "172.20.6.61"
          self.port = 9090
          self.transport = TBufferedTransport(TSocket(self.host, self.port))
          self.transport.open()
          self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
          self.client = Hbase.Client(self.protocol)


        def __del__(self):
          self.transport.close()

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@class="lb"]/ul/li')[0:]
		articles = []
		for news in newsurl:
			i = DemoItem()
			urltemp = news.xpath('a/@href').extract()
			url = "http://www.yos.com.cn/xwzx/qydt" + (len(urltemp)>0 and urltemp[0].strip()[1:] or '')
			i['url'] = url
			title = news.xpath('a/text()').extract()
			i['title'] = len(title)>0 and title[0].strip() or ''
			time = news.xpath('span/text()').extract()
			i['time'] = len(time)>0 and time[0] or ''
			i['siteName'] = 'yos'
			articles.append(i)
		return articles

