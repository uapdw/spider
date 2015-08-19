# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from group3.items import WebArticleItem 
from scrapy.http import Request
import datetime
import htmlfilter
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *
class ZongSWeiXinSpider(CrawlSpider):
	name = 'zongs_weixin'
	allowed_domains = ['sogou.com','mp.weixin.qq.com']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tDnsjWeiXin = infoDB.dnsj_weixin
	
	start_urls = ['http://weixin.sogou.com/weixin?query=%E5%AE%97%E7%94%B3&fr=sgsearch&type=2&w=01019900&sut=2190&sst0=1438238533209&lkt=0%2C0%2C0']
	rules = (
	Rule(SgmlLinkExtractor(allow=r'page=\d+', restrict_xpaths=('//*[@id="pagebar_container"]')),callback='parse_item',follow=True),
	)
        def __init__(self,**kw):
          super(ZongSWeiXinSpider,self).__init__(**kw)
          self.host = "172.20.6.61"
          self.port = 9090
          self.transport = TBufferedTransport(TSocket(self.host, self.port))
          self.transport.open()
          self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
          self.client = Hbase.Client(self.protocol)
          self.today = datetime.date.today()
          self.yesterday = (datetime.date.today() - datetime.timedelta(days=1))
          self.time_range = [self.today, self.yesterday]

        def __del__(self):
          self.transport.close()
	def parse_item(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@class="results"]/div[@class="wx-rb wx-rb3"]')[0:]
		items = []
		for news in newsurl:
				i = WebArticleItem()
				urltemp = news.xpath('div[@class="txt-box"]/h4/a/@href').extract()
				i['url'] = len(urltemp)>0 and urltemp[0].strip() or ''
				title = news.xpath('div[@class="txt-box"]/h4').extract()[0]
				i['title'] = htmlfilter.filterTags(title)
				abstract = news.xpath('div[@class="txt-box"]/p').extract()[0]
				i['abstract'] = htmlfilter.filterTags(abstract)
				items.append(i)
		for item in items:
				yield Request(item['url'],meta={'item':item},callback=self.parse_item01)
		

	def parse_item01(self, response):
		sel = Selector(response)
		i = response.meta['item']
                try:
                                pubTime = sel.xpath('//em[@id="post-date"]/text()').extract()[0]
                                match = re.match(u'\d+-\d+-\d+',pubTime,re.UNICODE)
                                if match:
                                                pubTime = match.group(0)
                                if pubTime:
                                                i['publishTime'] = datetime.datetime.strptime(pubTime, '%Y-%m-%d')
                                else:
                                                i['publishTime'] = datetime.datetime(1970,1,1)

                except:
                                pass

                if i['publishTime']:
                                pass
                                #if i['publishTime'].date() not in self.time_range:
                                #               return
                else:
                                i['publishTime'] = datetime.datetime(1970,1,1)
                try:
                                source = sel.xpath('//div[@class="rich_media_meta_list"]/a[@class="rich_media_meta rich_media_meta_link rich_media_meta_nickname"]/text()').extract()
                                i['source'] = len(source)>0 and source[0] or ''
                except:
                                pass
		if not i['source']:
                                i['source'] = ''
		i['author'] = ''
		i['keyWords'] = ''
		i['newstype'] = '微信'
		content = sel.xpath('//div[@class="rich_media_content"]').extract()[0]
		i['content'] = htmlfilter.filterTags(content)
		i['siteName'] = 'weixin.sogou.com'
		i['addTime'] = datetime.datetime.now()
		return i
