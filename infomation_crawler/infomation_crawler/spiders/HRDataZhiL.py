# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from infomation_crawler.items import HRDataItem
from scrapy.http import Request
import datetime
import pymongo
import re
class HRDataZhiLSpider(CrawlSpider):
	name = 'HRDataZhiL'
	allowed_domain = ['zhaopin.com']

	start_urls = ['http://jobs.zhaopin.com/all']

	rules = [
			Rule(SgmlLinkExtractor(allow=(r'http://jobs.zhaopin.com/all/p\d+'))),
			Rule(SgmlLinkExtractor(allow=(r'com/\d+.htm')),callback='parse_item'),
			]

	def parse_item(self, response):
		items = []
		sel = Selector(response)
		i = HRDataItem()
		i['url'] = response.url
		i['websource'] = 'www.zhaopin.com'
		#position_detail = sel.xpath('//ul[@class="terminal-ul clearfix"]/li')[0:]
		name_company = sel.xpath('//p[@class="company-name-t"]/a/text()').extract()
		i['name_company'] = len(name_company)>0 and name_company[0].strip() or ''
		scale_company = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()').extract()
		i['scale_company'] = len(scale_company)>0 and scale_company[0].strip() or ''
		type_company = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[2]/strong/text()').extract()
		i['type_company'] = len(type_company)>0 and type_company[0].strip() or ''

		industry_company = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[3]/strong/a/text()').extract()
		i['industry_company'] = len(industry_company)>0 and industry_company[0].strip() or ''
		website_company = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/a/text()').extract()
		i['website_company'] = len(website_company)>0 and website_company[0].strip() or ''
		address_company = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[5]/strong/text()').extract()
		if address_company:
			i['address_company'] = len(address_company)>0 and address_company[0].strip() or ''
		else:
			address_compan = sel.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/text()').extract()
			i['address_company'] = len(address_compan)>0 and address_compan[0].strip() or ''
		info_companylist = sel.xpath('//div[@class="tab-cont-box"]/div[2]/p[1]//span/text()').extract()

		info_company = len(info_companylist)>0 and info_companylist[0].strip() or ''
		for key in range(len(info_companylist)-1):
			info_company = info_company + '\n' + info_companylist[key+1].strip()
		i['info_company'] = len(info_company)>0 and info_company or ''
		name_position = sel.xpath('//div[@class="inner-left fl"]/h1/text()').extract()
		i['name_position'] = len(name_position)>0 and name_position[0].strip() or ''
		if sel.xpath('//div[@class="welfare-tab-box"]/span/text()').extract():
			keywords_positionlist = sel.xpath('//div[@class="welfare-tab-box"]/span/text()').extract()
			keywords_position = len(keywords_positionlist)>0 and keywords_positionlist[0].strip() or ''
			for key in range(len(keywords_positionlist)-1):
				keywords_position = keywords_position + '\n' + keywords_positionlist[key+1].strip()
		else:
			keywords_position = ''
		i['keywords_position'] = len(keywords_position)>0 and keywords_position or ''
		salary_position = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()
		i['salary_position'] = len(salary_position)>0 and salary_position[0].strip() or ''
		location_position = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()').extract()
		i['location_position'] = len(location_position)>0 and location_position[0].strip() or ''
		release_time = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract()
		i['release_time'] = len(release_time)>0 and release_time[0].strip() or ''
		nature_position = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()').extract()
		i['nature_position'] = len(nature_position)>0 and nature_position[0].strip() or ''
		experience_position = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()
		i['experience_position'] = len(experience_position)>0 and experience_position[0].strip() or ''
		education_demand = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()
		i['education_demand'] = len(education_demand)>0 and education_demand[0].strip() or ''
		number_demand = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[7]/strong/text()').extract()
		i['number_demand'] = len(number_demand)>0 and number_demand[0].strip() or ''
		type_position = sel.xpath('//ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract()
		i['type_position'] = len(type_position)>0 and type_position[0].strip() or ''
		try:
			jd_positionlist = sel.xpath('//div[@class="tab-cont-box"]/div[1]/div/text() | //div[@class="tab-cont-box"]/div[1]/p/span/text() | //div[@class="tab-cont-box"]/div[1]/p/text()').extract()
		except Exception,ex:
			jd_positionlist = ''
		if jd_positionlist:
			jd_position = len(jd_positionlist)>0 and jd_positionlist[0].strip() or ''
			for key in range(len(jd_positionlist)-1):
				jd_position = jd_position + '\n' + jd_positionlist[key+1].strip()
		else:
			jd_position = ''
		i['jd_position'] = len(jd_position)>0 and jd_position or ''
		dutypos = ''
		i['dutypos'] = ''
		i['requiremen_position'] = ''
		i['name_contact'] = ''
		i['tele_contact'] = ''
		i['email_contact'] = ''
		i['sex_requrment'] = ''
		i['pay_position'] = len(salary_position)>0 and salary_position[0].strip() or ''
		i['welfare_position'] = len(keywords_position)>0 and keywords_position or ''
		return i