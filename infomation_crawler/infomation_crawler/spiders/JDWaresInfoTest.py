# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.http import Request
from infomation_crawler.items import JDWaresInfoTestItem
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from xvfbwrapper import Xvfb
import datetime
import pymongo
import re
class JDWaresInfoTestSpider(CrawlSpider):
	name = 'JDWaresInfoTest'
	allowed_domain = ['jd.com','3.cn']
	conn = pymongo.Connection('localhost',27017)
	infoDB = conn.info
	tJDBaseInfo = infoDB.tJDBaseInfo
	listshop = tJDBaseInfo.find()
	urls = []
	for item in listshop:
		shopid = item['shopid']
		url = 'http://item.jd.com/' + shopid +'.html'
		urls.append(url)
	start_urls = urls
	def __init__(self):
		vdisplay = Xvfb()
		vdisplay.start()
		self.driver = webdriver.Firefox()

	'''
	rules = [
			Rule(SgmlLinkExtractor(allow=("/list.html\?cat=737%2C794%2C878&page=\d+&JL=6_0_0"))),
			Rule(SgmlLinkExtractor(allow=(r'http://item.jd.com/\d+.html'),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
	]

	rules = [
			Rule(SgmlLinkExtractor(allow=(r'http://item.jd.com/\d+.html'),restrict_xpaths=('//div[@id="plist"]')),callback='parse_item'),
			Rule(SgmlLinkExtractor(allow=("/list.html\?cat=737%2C794%2C878&page=\d+&JL=6_0_0"), restrict_xpaths=("//a[@class='next']"))),
			]
	'''

	def parse(self, response):
		item= JDWaresInfoTestItem()
		sel = Selector(response)
		self.driver.get(response.url)
		#pageSource = self.driver.page_source
		try:
			name = self.driver.find_element_by_xpath('//div[@class="seller-infor"]/a').get_attribute('title')
		except:
			name = self.driver.find_element_by_xpath('//h1').text

		#self.driver.close()
		item['name'] = name
		item['pt_name'] = 'JD'
		pt_sp_address = response.url
		item['pt_sp_address'] = pt_sp_address
		try:
			pinlei = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]/strong/a').text
			dalei = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]/span[1]/a[1]').text
			xiaolei = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]/span[1]/a[2]').text
			brand = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]/span[2]/a[1]').text
			danpin_name = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]/span[2]/a[2]').text
			danpin_code = self.driver.find_element_by_xpath('//div[@class="fl"]/span[2]').text
		except Exception,ex:
			print ex
		item['pinlei'] = pinlei
		item['dalei'] = dalei
		item['xiaolei'] = xiaolei
		item['brand'] = brand
		item['danpin_name'] = danpin_name
		item['danpin_code'] = danpin_code
		danpin_photo = sel.xpath('//div[@class="spec-items"]/ul/li/img/@src').extract()
		item['danpin_photo'] = len(danpin_photo)>0 and (',').join(danpin_photo) or ''
		danpin_introlist = sel.xpath('//ul[@id="parameter2"]/li/text()').extract()
		danpin_intro = len(danpin_introlist)>0 and danpin_introlist[0].strip() or ''
		for key in range(len(danpin_introlist)-1):
			danpin_intro = danpin_intro + ',' + danpin_introlist[key+1].strip()

		item['danpin_intro'] = danpin_intro
		list = sel.xpath('//div[@id="product-detail-2"]/table//tr/td/text()').extract()
		klist = [list[index] for index in range(0, len(list) - 1, 2)]
		vlist = [list[index] for index in range(1, len(list) - 1, 2)]
		specdict = {}
		for index in range(0, max(len(klist),len(vlist)) - 1):
			k = None
			v = None
			if index < len(klist):
				k = klist[index]
			if index < len(vlist):
				v = vlist[index]
			specdict[k] = v
		danpin_spec = ''
		for key, value in specdict.items():
			danpin_spec = danpin_spec + "\"%s\":\"%s\"" % (key, value) + ','
		item['danpin_spec'] = danpin_spec
		danpin_package = sel.xpath('//div[@id="product-detail-3"]/div[@class="item-detail"]/text()').extract()
		item['danpin_package'] = len(danpin_package)>0 and danpin_package[0] or ''
		danpin_after_sale = sel.xpath('//div[@id="product-detail-5"]/div[@class="item-detail"]/text()').extract()
		item['danpin_after_sale'] = len(danpin_after_sale)>0 and danpin_after_sale[0].strip() or ''
		danpin_slogan = self.driver.find_element_by_id('p-ad').text
		item['danpin_slogan'] = danpin_slogan
		try:
			danpin_info_detail_tmp = self.driver.find_elements_by_xpath('//div[@class="dd"]/div/a')
		except Exception,ex:
			print ex
		danpin_info_detailtmp =''
		for danpin_info_detail in danpin_info_detail_tmp:
			if danpin_info_detail.get_attribute('title'):
				danpin_info_detailtmp = danpin_info_detailtmp + danpin_info_detail.get_attribute('title') + ','
		item['danpin_info_detail'] = danpin_info_detailtmp

		price = self.driver.find_element_by_class_name("p-price").text
		item['danpin_price'] = price.replace(u'\uffe5','')

		danpin_pro_tmp = ''
		try:
			danpin_promotion = self.driver.find_elements_by_class_name("hl_red")
			for promotion in danpin_promotion:
				if promotion.text:
					danpin_pro_tmp = danpin_pro_tmp + promotion.text + ','
		except Exception,ex:
			print ex
			danpin_pro_tmp = ''
		item['danpin_promotion'] = danpin_pro_tmp

		id="store-prompt"
		try:
			danpin_fare = self.driver.find_element_by_xpath('//div[@id="store-prompt"]/a[2]').text
		except Exception,ex:
			danpin_fare = ''
		try:
			danpin_payment_method = self.driver.find_element_by_xpath('//div[@id="store-prompt"]/a[1]').get_attribute('title')
		except Exception,ex:
			danpin_payment_method = ''
		item['danpin_fare'] = len(danpin_fare)>0 and danpin_fare or ''
		item['danpin_payment_method'] = len(danpin_payment_method)>0 and danpin_payment_method or ''
		try:
			danpin_service_tips = self.driver.find_element_by_xpath('//ol[@class="tips-list clearfix"]/li').text
		except Exception,ex:
			print ex
		try:
			danpin_add_service = self.driver.find_element_by_xpath('//div[@class="service-type-yb"]//div[@class="item"]/a[2]').text
		except Exception,ex:
			danpin_add_service = ''
		try:
			danpin_carrier = self.driver.find_element_by_xpath('//div[@id="summary-service"]/div[@class="dd"]').text
		except Exception,ex:
			danpin_carrier = ''
		item['danpin_carrier'] = len(danpin_carrier)>0 and danpin_carrier or ''
		item['danpin_add_service'] = len(danpin_add_service)>0 and danpin_add_service or ''
		item['danpin_service_tips'] = len(danpin_service_tips)>0 and danpin_service_tips or ''
		#self.driver.find_element_by_class_name("btn-dbt").click()
		crediturl = 'http://baitiao.jd.com/ious/showLayer?price=' + item['danpin_price']  + '&prop2=&prop3=&src=1'
		return item
		#print '#' *40
		#print item['danpin_price']
		#yield Request(crediturl,meta={'item':item},callback=self.parseCredit)
	def __del__(self):
		self.driver.close()


	def parseCredit(self, response):
		sel = Selector(text=response.body)
		try:

			bai = sel.xpath('//div[@class="right-text"]/p[1]/span/text()').extract()
			bai_01 = sel.xpath('//div[@class="right-text"]/p[2]/span/text()').extract()[0].strip()
			baitiao = sel.xpath('//div[@class="bt-right"]/span/text()').extract()[0].strip() + bai[0].strip() + sel.xpath('//div[@class="right-text"]/p[1]/span/strong/text()').extract()[0].strip().replace(u'\xa5','') + bai[1].strip() + ',\n' + sel.xpath('//div[@class="right-text"]/p[2]/text()').extract()[0].strip() + sel.xpath('//div[@class="right-text"]/p[2]/span/strong/text()').extract()[0].strip() + bai_01

		except Exception,ex:
			baitiao = ""
		j = response.meta['item']
		j['danpin_credit_service'] = baitiao

		return j