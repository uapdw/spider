from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WeiBoItem
from scrapy.http import Request
import datetime
import pymongo
import re
class DnsjWeiBoSpider(CrawlSpider):
	name = 'dnsj_weibo'
	allowed_domains = ['zhongsou.com']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tDnsjNews = infoDB.dnsj_news
	
	start_urls = ['http://t.zhongsou.com/wb?w=%B4%F3%C4%EF%CB%AE%BD%C8&form_id=1&v=%D6%D0%CB%D1']
	
	def parse(self, response):
		sel = Selector(text=response.body)
		newsurl = sel.xpath('//div[@class="main_scenery_left"]/div[@class="godreply_on"]/div[@class="weibo_item clearfix"]')[0:]
		print newsurl
		articles = []
		for news in newsurl:
			i = WeiBoItem()
			urltemp = news.xpath('div[@class="weibo_touxiang"]/a/img/@src').extract()
			imageurl = "http://www.yonghe.com.cn" + (len(urltemp)>0 and urltemp[0].strip() or '')
			i['image'] = imageurl
			username = news.xpath('div[@class="weibo_right"]/h3/a/text()').extract()
			i['username'] = len(username)>0 and username[0].strip() or ''
			content = news.xpath('div[@class="weibo_right"]/p/text()').extract()
			content_data = ''.join(content).strip()
			i['content'] = len(content)>0 and content_data or ''
			source =  news.xpath('div[@class="weibo_right"]/div[@class="weibo_handle clearfix"]/a/text()').extract()
			source_data = ' '.join(source).strip()
			print source_data
			i['source'] = len(source)>0 and source_data or ''
			articles.append(i)
		return articles
	  

