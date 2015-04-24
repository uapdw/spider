from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import datetime
import pymongo
import re
class CnddrSpider(CrawlSpider):
	name = 'cnddr'
	allowed_domains = ['cnddr.com']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news
	start_urls = ['http://www.cnddr.com/news_1_1.html']

	def parse(self, response):
		sel = Selector(response)
		items=[]
		newsurl = sel.xpath('//div[@class="news_ul"]/ul/li')[0:]
		for news in newsurl:
			i = DemoItem()
			urltemp = news.xpath('div[@class="news_t"]/a/@href').extract()[0]
			url = "http://www.cnddr.com/" + urltemp
			i['url'] = url
			title = news.xpath('div[@class="news_t"]/a/@title').extract()
			i['title'] = len(title)>0 and title[0].strip() or ''
			time = news.xpath('div[@class="date"]/text()').extract()
			i['time'] = len(time)>0 and time[0].strip() or ''
			i['siteName'] = 'cnddr'
			items.append(i)
		return items

