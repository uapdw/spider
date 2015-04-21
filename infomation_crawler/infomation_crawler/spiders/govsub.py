# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import GovSubItem
from scrapy.http import Request
import datetime
import pymongo
import time
import re
class GovSubSpider(CrawlSpider):
	name = 'govsub'
	allowed_domains = ['ccgp.gov.cn']
	urls = []
	global YEAR,MONTH,DATE 
	YEAR = time.strftime('%Y',time.localtime(time.time()))
	MONTH = time.strftime('%m',time.localtime(time.time()))
	DATE = time.strftime('%d',time.localtime(time.time()))
	urls.append(
			'http://search.ccgp.gov.cn/dataB.jsp?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + YEAR + '%3A'+ MONTH +'%3A'+ DATE +'&end_time='+ YEAR +'%3A'+ MONTH +'%3A'+ DATE +'&timeType=0&displayZone=&zoneId=&agentName=')
	start_urls = urls

	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		content = sel.xpath('//div[@class="vT_detail_content w760c"]').extract()
		i['content'] = len(content)>0 and content[0] or ''
		source = "中国政府采购网"
		i['source'] = source
		return i

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//ul[@class="vT-srch-result-list-bid"]/li')[0:]
		articles = []
		for news in newsurl:
			i = GovSubItem()
			buyer = news.xpath('span/text()').extract()
			i['buyer'] = len(buyer) > 0 and buyer[0].split('|')[1].strip()[4:] or ''
			i['agent'] = len(buyer) > 0 and buyer[0].split('|')[2].strip()[5:] or ''
			i['publishTime'] = len(buyer) > 0 and buyer[0].split('|')[0].strip().split(' ')[0].replace('.','-') or ''
			keyWordslist = news.xpath('span/strong/text()').extract()
			kwtmp = news.xpath('span/a/text()').extract()
			keyWordslist[1] = kwtmp[0]
			keyWords = len(keyWordslist)>0 and keyWordslist[0].strip() or ''
			for key in range(len(keyWordslist)-1):
				keyWords = keyWords + '|' + keyWordslist[key + 1].strip()
			i['keyWords'] = keyWords
			abstract = news.xpath('p/text()').extract()
			i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''
			urltemp = news.xpath('a/@href').extract()
			i['url'] = len(urltemp)>0 and urltemp[0].strip() or ''
			title = news.xpath('a/text()').extract()
			i['title'] = len(title) > 0 and title[0].strip() or ''
			articles.append(i)
		for item in articles:
			yield Request(item['url'],meta={'item':item},callback=self.parse_item)
		page = sel.xpath('//p[@class="pager"]/script/text()').extract()[0].strip().split(',')[0].split(':')[-1].encode('utf-8')
		for index in range(2,int(page)):
			url = 'http://search.ccgp.gov.cn/dataB.jsp?searchtype=2&page_index='+ str(index) +'&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + YEAR + '%3A'+ MONTH +'%3A'+ DATE +'&end_time='+ YEAR +'%3A'+ MONTH +'%3A'+ DATE +'&timeType=0&displayZone=&zoneId=&agentName='
			yield Request(url, callback=self.parse)
	  

