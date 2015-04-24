from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import datetime
import pymongo
import re
class McdonaldsSpider(CrawlSpider):
	name = 'mcdonalds'
	allowed_domains = ['mcdonalds.com.cn']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news
	
	start_urls = ['http://www.mcdonalds.com.cn/cn/ch/newsroom/news.html']

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//dl[@class="news"]/dt')[0:]
		articles = []
		for news in newsurl:
			i = DemoItem()
			urltemp = news.xpath('@id').extract()
			url = "http://www.mcdonalds.com.cn" + (len(urltemp)>0 and urltemp[0].strip() or '') + ".html"
			i['url'] = url
			title = news.xpath('a/text()').extract()
			i['title'] = len(title)>0 and title[0].strip() or ''
			time = news.xpath('@id').re(r'\d{8}')[0].strip()
			i['time'] = time[0:4] + '-' + time[4:6] + '-' + time[-2:]
			i['siteName'] = 'mcdonalds'
			articles.append(i)
		return articles

