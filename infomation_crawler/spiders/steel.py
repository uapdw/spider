import re
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import SteelIndexNumberItem

class SteelSpider(Spider):
    name = 'steel'
    allowed_domains = ['glinfo.com']
    start_urls = ['http://index.glinfo.com/xpic/report.ms?tabName=GANGCAIZONGHE&typeName=%25u94A2%25u6750%25u7EFC%25u5408&dateType=day&startTime=1980-07-01&endTime=2014-07-24']


    def parse(self, response):
        sel = Selector(response)
	trList = sel.xpath('//tr')
	pubDate = []
	indexNum = []
	for index,tr in enumerate(trList):
	  arrDate = tr.xpath('./td[contains(@bgcolor,"#FFFFFF")][1]/text()').extract()
	  arrIndex = tr.xpath('./td[contains(@bgcolor,"#FFFFFF")][2]/text()').extract()
	  if len(arrDate) < 1:
	    pass
	  else:
	    pubDate.append(arrDate[0].strip())
	    indexNum.append(arrIndex[0].strip())
	  
        i = SteelIndexNumberItem()
        i['pubDate'] = pubDate
        i['indexNumber'] = indexNum
        return i
