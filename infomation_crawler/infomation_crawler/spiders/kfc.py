from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import json
import datetime
import pymongo
import re
class KFCSpider(CrawlSpider):
	name = 'kfc'
	allowed_domains = ['kfc.com.cn']

	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news

	urls = []
	queryid= [237,235,233,222,212,207,201,199,192,190]
	for i in queryid:
		urls.append('http://www.kfc.com.cn/kfccda/ashx/GetNewsInfo.ashx?id=%s' % i)
	start_urls = urls
	
	def parse(self, response):
		i = DemoItem()
		items = []
		json_d = response.body[1:-1]
		json_data = json.loads(json_d)
		i['title'] = json_data['Title']
		i['time'] = json_data['Addtime']
		i['url'] = response.url
		i['siteName'] = 'kfc'
		return i

