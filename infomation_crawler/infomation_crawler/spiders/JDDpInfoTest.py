# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.http import Request
from infomation_crawler.items import JDDpInfoTestItem
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from xvfbwrapper import Xvfb
from BeautifulSoup import BeautifulSoup
import datetime
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class JDDpInfoTestSpider(CrawlSpider):
	name = 'JDDpInfoTest'
	allowed_domain = ['jd.com']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tJDBaseInfo = infoDB.tJDBaseInfo
	listshop = tJDBaseInfo.find()
	#start_urls = ['http://item.jd.com/1117284441.html']

	urls = []
	for item in listshop:
		shopid = item['shopid']
		url = 'http://item.jd.com/' + shopid +'.html'
		urls.append(url)
		#print url
	start_urls = urls

	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)

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
	def __del__(self):
		self.driver.close()
		self.transport.close()

	def parse(self, response):
		item= JDDpInfoTestItem()
		sel = Selector(response)
		self.driver.get(response.url)
		#file = open('/tmp/los.html','w')
		page = self.driver.page_source
		soup = BeautifulSoup(page.encode('utf-8'))
		try:
			name = soup.find("a",{"class":"name"}).text
		except Exception,ex:
			name = ''
		try:
			sp_score = soup.find("span",{"class":"score-desc"}).find("em").text
		except Exception,ex:
			sp_score = ''
		try:
			url = soup.find("a",{"class":"name"}).get('href')
		except Exception,ex:
			url = ''
		try:
			score_total = soup.find("div",{"class":"score-sum"}).text
		except Exception,ex:
			score_total = ''
		try:
			sp_compare = soup.findAll("em",{"class":"percent"})[0].text
		except Exception,ex:
			sp_compare = ''
		try:
			service_score = soup.findAll("em",{"class":"number"})[2].text
		except Exception,ex:
			service_score = ''
		try:
			service_compare = soup.findAll("em",{"class":"percent"})[1].text
		except Exception,ex:
			service_compare = ''
		try:
			eff_score = soup.findAll("em",{"class":"number"})[3].text
		except Exception,ex:
			eff_score = ''
		try:
			eff_compare = soup.findAll("em",{"class":"percent"})[2].text
		except Exception,ex:
			eff_compare = ''
		try:
			Company_name = soup.find("span",{"class":"text J-shop-name"}).text
		except Exception,ex:
			Company_name = ''
		try:
			Company_city = soup.find("span",{"class":"text J-shop-address"}).text
		except Exception,ex:
			Company_city = ''
		try:
			suport_service = ''
			Surport_service = soup.find("dl",{"class":"jd-service"}).findAll('a')
			for surport in Surport_service:
				suport_service = suport_service + surport.text + ','
		except Exception,ex:
			suport_service = ''
		try:
			service_inf = soup.find("span",{"class":"text J-shop-phone"}).text
		except Exception,ex:
			service_inf = ''
		item['pt_name'] = 'JD'
		item['name'] = name
		item['url'] = url
		item['score_total'] = score_total
		item['sp_score'] = sp_score
		item['sp_compare'] = sp_compare
		item['service_score'] = service_score
		item['service_compare'] = service_compare
		item['eff_score'] = eff_score
		item['eff_compare'] = eff_compare
		item['Company_name'] = Company_name
		item['Company_city'] = Company_city
		item['Surport_service'] = suport_service
		item['service_inf'] = service_inf
		#pageSource = self.driver.page_source
		#file.write(page.encode('utf-8'))
		#self.driver.find_element_by_xpath('//i[@class="arrow-show-more J-show-score-detail"]').click()
		#name = self.driver.find_element_by_class_name("number").text
		#name = self.driver.find_element_by_xpath('//div[@class="score-sum"]/em').text
		return item
