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
class ZongSBaiDuSpider(CrawlSpider):
	name = 'zongs_baidu'
	allowed_domains = ['baidu.com']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tDnsjWeiXin = infoDB.dnsj_weixin
	
	start_urls = ['http://news.baidu.com/ns?word=%D7%DA%C9%EA&tn=news&from=news&cl=2&rn=20&ct=1','http://news.baidu.com/ns?word=%D0%C2%B4%F3%D6%DE%B1%BE%CC%EF&tn=news&from=news&cl=2&rn=20&ct=1','http://news.baidu.com/ns?word=%CE%E5%D1%F2%B1%BE%CC%EF&tn=news&from=news&cl=2&rn=20&ct=1','http://news.baidu.com/ns?word=%C7%AE%BD%AD%C4%A6%CD%D0&tn=news&from=news&cl=2&rn=20&ct=1','http://news.baidu.com/ns?word=%C2%A1%F6%CE%CD%A8%D3%C3&tn=news&from=news&cl=2&rn=20&ct=1','http://news.baidu.com/ns?word=%B4%F3%B3%A4%BD%AD&tn=news&from=news&cl=2&rn=20&ct=1']
	rules = (
	Rule(SgmlLinkExtractor(allow=r'pn=\d+', restrict_xpaths=('//*[@id="page"]')),callback='parse_item',follow=True),
	)
        def __init__(self,**kw):
          super(ZongSBaiDuSpider,self).__init__(**kw)
          self.host = "172.20.6.61"
          self.port = 9090
          self.transport = TBufferedTransport(TSocket(self.host, self.port))
          self.transport.open()
          self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
          self.client = Hbase.Client(self.protocol)
          self.may = (datetime.date.today() - datetime.timedelta(days=90)) 

        def __del__(self):
          self.transport.close()
	def parse_item(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@id="content_left"]//div[@class="result"]')[0:]
		items = []
		re_p = re.compile('<\s*p[^>]*>[^<]*<\s*/\s*p\s*>',re.I)
		for news in newsurl:
				i = WebArticleItem()
				urltemp = news.xpath('h3[@class="c-title"]/a/@href').extract()
				i['url'] = len(urltemp)>0 and urltemp[0].strip() or ''
				title = news.xpath('h3[@class="c-title"]').extract()[0]
				i['title'] = htmlfilter.filterTags(title)
				abstract = news.xpath('div[1]').extract()[0]
				_abstract = re_p.sub('',abstract)
				i['abstract'] = htmlfilter.filterTags(abstract)
				
				pubtime = news.xpath('//p[@class="c-author"]/text()').extract()[0].replace(u'\xa0','@').split('@')[-1]
				match = re.match(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)',pubtime,re.UNICODE)
				if match:
						pubtime = match.group(1) + '-' + match.group(2) + '-' + match.group(3) + ' ' + match.group(4) + ':' + match.group(5)
				else:
						pubtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
				i['publishTime'] = datetime.datetime.strptime(pubtime, '%Y-%m-%d %H:%M')
                		if i['publishTime']:
                                		if i['publishTime'].date() < self.may:
								return
				else:
                                		i['publishTime'] = datetime.datetime(1970,1,1)
				try:
						source = news.xpath('//p[@class="c-author"]/text()').extract()[0].replace(u'\xa0','@').split('@')[0]
						i['source'] = len(source)>0 and source or ''
				except:
                                                pass
				if not i['source']:
                                		i['source'] = ''
				i['author'] = ''
				i['keyWords'] = ''
				i['newstype'] = '通用'
				i['siteName'] = 'news.baidu.com'
				i['content'] = i['abstract']
				i['addTime'] = datetime.datetime.now()
				return i
							
						
		

