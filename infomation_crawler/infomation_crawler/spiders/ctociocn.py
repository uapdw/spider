from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class CtocioCNSpider(CrawlSpider):
	name = 'ctociocn'
	allowed_domains = ['ctocio.com.cn']
	start_urls = ['http://www.ctocio.com.cn/','http://server.ctocio.com.cn/','http://news.ctocio.com.cn/',
			'http://bigdata.ctocio.com.cn/','http://mobile.ctocio.com.cn/','http://storage.ctocio.com.cn/',
			'http://database.ctocio.com.cn/','http://esoft.ctocio.com.cn/','http://networking.ctocio.com.cn/',
			'http://security.ctocio.com.cn/','http://os.ctocio.com.cn/','http://cio.ctocio.com.cn/','http://virtualization.ctocio.com.cn/']
	
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tWebArticles = infoDB.web_articles
	rules = (
			Rule(SgmlLinkExtractor(allow=r'(www|server|news|bigdata|mobile|storage|database|esoft|networking|security|os|cio|virtualization)\.ctocio\.com\.cn/\d+/\d+\.shtml'), callback='parse_item'),
  )
        def __init__(self,**kw):
          super(CtocioCNSpider,self).__init__(**kw)
          self.host = "172.20.6.61"
          self.port = 9090
          self.transport = TBufferedTransport(TSocket(self.host, self.port))
          self.transport.open()
          self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
          self.client = Hbase.Client(self.protocol)
      
      
        def __del__(self):
          self.transport.close()
	
	def parse_item(self, response):
		print "enter ctocioCN_parse_item...."
		sel = Selector(response)
		i = WebArticleItem()
		title = sel.xpath('//h2[@class="maintitle"]/text()').extract()
		i['title'] = len(title)>0 and title[0].strip() or ''
		
		i['url'] = response.url
		pubTime = sel.xpath('//div[@class="time"]/span[3]/text()').extract()
		source = sel.xpath('//div[@class="time"]/span[2]/text()').extract()
		author = sel.xpath('//div[@class="time"]/span[1]/text()').extract()
		i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
		i['source'] = len(source)>0 and source[0].split(u'\uff1a')[1] or ''
		i['author'] = len(author)>0 and author[0].split(u'\uff1a')[1] or ''
		i['abstract'] = ''
		
		keyWords = sel.xpath('//h2[@class="keyword"]/em/text()').extract()
		i['keyWords'] = len(keyWords)>0 and keyWords[0].strip().replace(',','|') or ''
		
		content = sel.xpath('//div[@class="artical"]').extract()
		i['content'] = len(content)>0 and content[0] or ''
		i['siteName'] = 'ctocio'
		
		i['addTime'] = datetime.datetime.now()
		
		return i
