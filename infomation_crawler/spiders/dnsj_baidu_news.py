from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import DemoItem
from scrapy.http import Request
import datetime
import pymongo
import re
class DnsjBaiDuSpider(CrawlSpider):
	name = 'DnsjBaiDu'
	allowed_domains = ['baidu.com']

	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news

	start_urls = ['http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%E5%A4%A7%E5%A8%98%E6%B0%B4%E9%A5%BA']

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@id="content_left"]/ul/li')[0:]
		articles = []
		for news in newsurl:
			i = DemoItem()
			urltemp = news.xpath('h3/a/@href').extract()
			i['url'] = len(urltemp)>0 and urltemp[0].strip() or ''
			title_temp = news.xpath('h3/a/text()').extract()
			title_em = news.xpath('h3/a/em/text()').extract()
			if len(title_em) > 1:
				title = title_temp[0].strip() + title_em[0] + title_temp[1].strip() + title_em[1] + title_temp[2].strip()
			elif len(title_temp) > 1:
				title = title_temp[0].strip() + title_em[0] + title_temp[1].strip()
			else:
				title = title_temp[0].strip() + (len(title_em)>0 and title_em[0] or '')
			i['title'] = title
			date = news.xpath('div[1]/p[@class="c-author"]/text()').extract()
			time = len(date)>0 and date[0].strip().replace(u'\xa0','@').split('@') or ''
			i['time'] = len(time)>0 and time[-1].split(' ')[0] or ''
			i['siteName'] = 'baidu'
			articles.append(i)

		return articles
