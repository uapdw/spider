from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import datetime
import pymongo
import re
class YongheSpider(CrawlSpider):
	name = 'yonghe'
	allowed_domains = ['yonghe.com.cn']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news
	
	start_urls = ['http://www.yonghe.com.cn/index.php/Index/newscenter']

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@class="listmain_right"]/ul/li')[0:]
		articles = []
		for news in newsurl:
			i = DemoItem()
			urltemp = news.xpath('a/@href').extract()
			url = "http://www.yonghe.com.cn" + (len(urltemp)>0 and urltemp[0].strip() or '')
			i['url'] = url
			title = news.xpath('a/text()').extract()
			i['title'] = len(title)>0 and title[0].strip() or ''
			time = news.xpath('span/text()').extract()
			i['time'] = len(time)>0 and time[0] or ''
			i['siteName'] = 'yonghe'
			articles.append(i)
		return articles

