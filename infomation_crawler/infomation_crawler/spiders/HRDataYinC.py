# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from infomation_crawler.items import HRDataItem
from scrapy.http import Request
import datetime
import pymongo
import re
class HRDataYinCSpider(CrawlSpider):
	name = 'HRDataYinC'
	allowed_domain = ['chinahr.com','hrm.cn']

	start_urls = ['http://www.chinahr.com/jobs/10000/']

	rules = [
			Rule(SgmlLinkExtractor(allow=(r'jobs/10000/\d+/'),restrict_xpaths=('//a[@class="paging_r"]'))),
			Rule(SgmlLinkExtractor(allow=(r'job/.*.html')),callback='parse_item'),
			]

	def parse_item(self, response):
		items = []
		sel = Selector(response)
		i = HRDataItem()
		i['url'] = response.url
		i['websource'] = 'www.chinahr.com'
		#position_detail = sel.xpath('//ul[@class="terminal-ul clearfix"]/li')[0:]
		name_company = sel.xpath('//h2[@class="detail_R_cName"]/text()').extract()
		i['name_company'] = len(name_company)>0 and name_company[0].strip() or ''
		scale_company = sel.xpath('//ul[@class="detail_R_cList"]/li[3]/text()').extract()
		i['scale_company'] = len(scale_company)>0 and scale_company[0].strip() or ''
		type_company = sel.xpath('//ul[@class="detail_R_cList"]/li[2]/text()').extract()
		i['type_company'] = len(type_company)>0 and type_company[0].strip() or ''

		industry_company =  sel.xpath('//ul[@class="detail_R_cList"]/li[1]/text()').extract()
		i['industry_company'] = len(industry_company)>0 and industry_company[0].strip() or ''
		website_company =  sel.xpath('//ul[@class="detail_R_cList"]/li[6]/a/text()').extract()
		i['website_company'] = len(website_company)>0 and website_company[0].strip() or ''
		i['address_company'] = ''
		info_companylist = sel.xpath('//div[@class="tab-cont-box"]/div[2]/p[1]//span/text()').extract()

		i['info_company'] = ''
		name_position = sel.xpath('//h1[@class="company_name"]/a/text()').extract()
		i['name_position'] = len(name_position)>0 and name_position[0].strip() or ''
		if sel.xpath('//ul[@class="welf_list clear toggleWelfL"]/li').extract():
			keywords_positionlist = sel.xpath('//ul[@class="welf_list clear toggleWelfL"]/li/text()').extract()
			keywords_position = len(keywords_positionlist)>0 and keywords_positionlist[0].strip() or ''
			for key in range(len(keywords_positionlist)-1):
				if keywords_positionlist[key+1]:
					keywords_position = keywords_position + '\n' + keywords_positionlist[key+1].strip()
		else:
			keywords_position = ''
		i['keywords_position'] = len(keywords_position)>0 and keywords_position or ''
		salary_position = sel.xpath('//div[@class="detail_C_info"]/span/strong/text()').extract()
		i['salary_position'] = len(salary_position)>0 and salary_position[0].strip() or ''
		location_position = sel.xpath('//p[@class="infoMa"]/a/text()').extract()
		i['location_position'] = len(location_position)>0 and location_position[0].strip() or ''
		release_time = sel.xpath('//span[@class="detail_C_Date fl"]/text()').extract()
		i['release_time'] = len(release_time)>0 and release_time[0].split(u'\uff1a')[1].strip() or ''
		nature_position = sel.xpath('//div[@class="job_desc"]/p[2]/text()').extract()
		i['nature_position'] = len(nature_position)>0 and nature_position[0].split(u'\uff1a')[1].strip() or ''
		experience_position = sel.xpath('//div[@class="detail_C_info"]/span[3]/text()').extract()
		i['experience_position'] = len(experience_position)>0 and experience_position[0].strip() or ''
		education_demand = sel.xpath('//div[@class="detail_C_info"]/span[2]/text()').extract()
		i['education_demand'] = len(education_demand)>0 and education_demand[0].strip() or ''
		number_demand = sel.xpath('//div[@class="detail_C_info"]/span[4]/text()').extract()
		i['number_demand'] = len(number_demand)>0 and number_demand[0].split(u'\uff1a')[1].strip() or ''
		type_position = sel.xpath('//ul[@class="detail_R_cList"]/li[1]/text()').extract()
		i['type_position'] = len(type_position)>0 and type_position[0].strip() or ''
		try:
			jd_positionlist = sel.xpath('//p[@class="infoMa"]/text() | //p[@class="infoMa"]/a/text()').extract()
		except Exception,ex:
			jd_positionlist = ''
		if jd_positionlist:
			jd_position = len(jd_positionlist)>0 and jd_positionlist[0].strip() or ''
			for key in range(len(jd_positionlist)-1):
				jd_position = jd_position + jd_positionlist[key+1].replace(u'\xa0','').replace('\n','').strip()
		else:
			jd_position = ''
		i['jd_position'] = len(jd_position)>0 and jd_position or ''
		if sel.xpath('//p[@class="detial_jobSec"]')[0:]:
			duty = sel.xpath('//p[@class="detial_jobSec"]')[0:]
			dutyposition = duty[0].xpath('text() | a/text()').extract()
			dutytmp = len(dutyposition)>0 and dutyposition[0].strip() or ''
			for key in range(len(dutyposition)-1):
				dutytmp = dutytmp  + dutyposition[key+1].replace('\n','').strip()
			i['dutypos'] = len(dutytmp)>0 and dutytmp or ''
			if len(duty) == 1:
				i['requiremen_position'] = ''
				i['welfare_position'] = ''
			else:
				requiremenlist = duty[1].xpath('text() | a/text()').extract()
				requiremen = len(requiremenlist)>0 and requiremenlist[0].strip() or ''
				for key in range(len(requiremenlist)-1):
					requiremen = requiremen  + requiremenlist[key+1].replace('\n','').strip()
				i['requiremen_position'] = len(requiremen)>0 and requiremen or ''
				welfarelist = duty[1].xpath('text() | a/text()').extract()
				welfare = len(welfarelist)>0 and welfarelist[0].strip() or ''
				for key in range(len(welfarelist)-1):
					welfare =  welfare + welfarelist[key+1].replace('\n','').strip()
				i['welfare_position'] = len(welfare)>0 and welfare or ''
		else:
			i['dutypos'] = ''
			i['requiremen_position'] = ''
			i['welfare_position'] = ''
		i['name_contact'] = ''
		i['tele_contact'] = ''
		i['email_contact'] = ''
		if sel.xpath('//p[@class="sub_infoMa"]/span[2]/text()').extract():
			sex_requrment = sel.xpath('//p[@class="sub_infoMa"]/span[2]/text()').extract()
			i['sex_requrment'] = len(sex_requrment)>0 and sex_requrment[0].split(u'\uff1a')[1].strip() or ''
		else:
			sex_requrment = sel.xpath('//p[@class="sub_infoMa"]/span/text()').extract()
			i['sex_requrment'] = len(sex_requrment)>0 and sex_requrment[0].strip() or ''

		i['pay_position'] = len(salary_position)>0 and salary_position[0].strip() or ''
		return i