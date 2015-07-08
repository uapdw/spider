# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from infomation_crawler.items import JDBaseInfoItem
import datetime
import pymongo
import re
class JDBaseInfoSpider(CrawlSpider):
	name = 'JDBaseInfo'
	allowed_domain = ['jd.com']
	start_urls=["http://list.jd.com/list.html?cat=737,794,878"]
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	#remove = infoDB.tJDBaseInfo.remove({})
	tJDBaseInfo = infoDB.tJDBaseInfo
	rules = [
			Rule(SgmlLinkExtractor(allow=("/list.html\?cat=737%2C794%2C878&page=\d+&JL=6_0_0"))),
			Rule(SgmlLinkExtractor(allow=(r'http://item.jd.com/\d+.html\#comments-list'),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
			]
	def parse_item(self, response):
	 item= JDBaseInfoItem()
	 sel = Selector(response)
	 shopid = response.url.decode('utf8').split('/')[-1].split('.')[0]
	 shopurl = response.url
	 item['shopurl'] = shopurl
	 item['shopid'] = shopid
	 return item
