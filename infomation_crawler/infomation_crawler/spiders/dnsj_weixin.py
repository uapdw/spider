from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WeiXinItem
from scrapy.http import Request
import datetime
import pymongo
import re
class DnsjWeiXinSpider(CrawlSpider):
	name = 'dnsj_weixin'
	allowed_domains = ['sogou.com','mp.weixin.qq.com']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjWeiXin = infoDB.dnsj_weixin
	
	start_urls = ['http://weixin.sogou.com/weixin?query=%E5%A4%A7%E5%A8%98%E6%B0%B4%E9%A5%BA&_asf=www.sogou.com&_ast=&w=01015002&p=40040100&fr=sgsearch&ie=utf8&type=2&oq=%E5%A4%A7%E5%A8%98&ri=0&sourceid=sugg&stj=0%3B4%3B0%3B0&stj2=0&stj0=0&stj1=4&hp=20&hp1=&sut=4092&sst0=1422346883844&lkt=0%2C0%2C0']

	def parse_item(self, response):
		sel = Selector(response)
		i = response.meta['item']
		print i
		time = sel.xpath('//em[@id="post-date"]/text()').extract()
		i['time'] = len(time)>0 and time[0].strip() or ''
		print i['time']
		return i

	def parse(self, response):
		sel = Selector(response)
		newsurl = sel.xpath('//div[@class="results"]/div[@class="wx-rb wx-rb3"]')[0:]
		articles = []
		for news in newsurl:
			i = WeiXinItem()
			imageurl = news.xpath('div[@class="img_box2"]/a/img/@src').extract()
			i['image'] = len(imageurl) > 0 and imageurl[0].strip() or ''
			urltemp = news.xpath('div[@class="txt-box"]/h4/a/@href').extract()
			i['url'] = len(urltemp)>0 and urltemp[0].strip() or ''
			title = news.xpath('div[@class="txt-box"]/h4/a/em/text()|div[@class="txt-box"]/h4/a/text()').extract()
			title_data = len(title)>0 and ''.join(title).strip() or ''
			i['title'] = title_data
			content = news.xpath('div[@class="txt-box"]/p/em/text()|div[@class="txt-box"]/p/text()').extract()
			content_data = len(content)>0 and ''.join(content).strip() or ''
			i['content'] = content_data
			source = news.xpath('div[@class="txt-box"]/div[@class="s-p"]/a/@title').extract() 
			i['source'] = len(source)>0 and source[0].strip() or ''
			articles.append(i)
		for item in articles:
			print item['url']
			yield Request(item['url'],meta={'item':item},callback=self.parse_item)

	  

