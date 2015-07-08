# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import scrapy
from infomation_crawler.items import JDWaresInfoItem
import datetime
import pymongo
import re
class JDWaresInfoSpider(Spider):
	name = 'JDWaresInfo'
	allowed_domain = ['jd.com','3.cn']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tJDBaseInfo = infoDB.tJDBaseInfo
	listshop = tJDBaseInfo.find()

	urls = []
	for item in listshop:
		shopid = item['shopid']
		url = 'http://item.jd.com/' + shopid +'.html'
		urls.append(url.encode('utf8'))
	start_urls = urls
	#print start_urls

	#start_urls = ['http://item.jd.com/751624.html']
	def start_requests(self):
		for url in self.start_urls:
			yield Request(url, self.parse, meta={
				'splash': {
					  'endpoint': 'render.html',
						#'args': {'wait': 0.5,'render_all': 1,}
					},
				'url':url
				})
	def parse(self, response):
		return self.parse_item(response)
	def parse_item(self, response):
		item = JDWaresInfoItem()
		sel = Selector(response)

		#print response.meta['url']

		item['pt_name'] = 'jd'
		pt_sp_address = response.meta['url']
		item['pt_sp_address'] = pt_sp_address
		name = sel.xpath('//div[@class="seller-infor"]/a/@title').extract()
		item['name'] = len(name)>0 and name[0] or ''
		pinlei = sel.xpath('//div[@class="breadcrumb"]/strong/a/text()').extract()
		item['pinlei'] = len(pinlei)>0 and pinlei[0] or ''
		dalei = sel.xpath('//div[@class="breadcrumb"]/span[1]/a[1]/text()').extract()
		item['dalei'] = len(dalei)>0 and dalei[0] or ''
		xiaolei = sel.xpath('//div[@class="breadcrumb"]/span[1]/a[2]/text()').extract()
		item['xiaolei'] = len(xiaolei)>0 and xiaolei[0] or ''
		print item['xiaolei']
		print '#' * 40
		brand = sel.xpath('//div[@class="breadcrumb"]/span[2]/a[1]/text()').extract()
		item['brand'] = len(brand)>0 and brand[0] or ''
		danpin_name = sel.xpath('//div[@class="breadcrumb"]/span[2]/a[2]/text()').extract()
		item['danpin_name'] = len(danpin_name)>0 and danpin_name[0] or ''
		danpin_code = sel.xpath('//div[@class="fl"]/span[2]/text()').extract()
		item['danpin_code'] = len(danpin_code)>0 and danpin_code[0] or ''
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
		danpin_slogan = sel.xpath('//h1/text()').extract()
		item['danpin_slogan'] = len(danpin_slogan)>0 and danpin_slogan[0] or ''
		danpin_info_detail_tmp = sel.xpath('//script/text()').extract()[0].encode('utf-8').split(';')[0]
		if re.findall(r'colorSize:.*]',danpin_info_detail_tmp):
			danpin_info_detail = re.findall(r'colorSize:.*]',danpin_info_detail_tmp)[0].split('"')[5].decode('utf8')
		else:
			danpin_info_detail = ''
		item['danpin_info_detail'] = len(danpin_info_detail)>0 and danpin_info_detail[0] or ''
		danpin_service_tips =re.findall(r'tips:.*]',danpin_info_detail_tmp)[0].split('"')[5].decode('utf8')
		print danpin_service_tips
		item['danpin_service_tips'] = danpin_service_tips
		price = sel.xpath('//*[@id="jd-price"]/text()').extract()
		print price
		item['danpin_price'] = len(price)>0 and price.replace(u'\uffe5','') or ''
		#print item['danpin_price']
'''
	def parsefare(self, response):
		sel = Selector(text=response.body)
		fare = response.body
		try:
			#tmp = re.findall(r'\d+\xc3\xe2\xd4\xcb\xb7\xd1',fare)[0]
			danpin_fare = len(re.findall(r'"showName":.*,',fare)) >0 and re.findall(r'\d+\xc3\xe2\xd4\xcb\xb7\xd1',fare)[0] or ''

		except Exception,ex:
			print ex;
			danpin_fare = ''
		try:
			payment = re.findall(r'"iconTip":".*?,',unicode( fare , errors='ignore'))
			danpin_payment_method = len(payment)>0 and payment[1].split(':')[1].replace('"','').replace(',','') or ''
		except Exception,ex:
			print ex;
			danpin_payment_method = ''
		i = response.meta['item']
		i['danpin_fare'] = unicode( danpin_fare , errors='ignore')
		i['danpin_payment_method'] = danpin_payment_method
		price_id = i['pt_sp_address'].decode('utf8').split('/')[-1].split('.')[0]
		priceurl = 'http://p.3.cn/prices/get?skuid=J_' + price_id + 'J_'
		r01 = Request(priceurl,callback=self.parsePrice)
		r01.meta['item'] = i
		yield r01
	def parsePrice(self, response):
		sel = Selector(text=response.body)

		try:
			price = sel.xpath("//text()").extract()[0].encode('utf-8').split('"')[7]
		except Exception,ex:
			print ex;
			price = 0
		i = response.meta['item']
		i['danpin_price'] = price
		crediturl = 'http://baitiao.jd.com/ious/showLayer?price=' + price  + '&prop2=&prop3=&src=1'
		r02 = Request(crediturl,callback=self.parseCredit)
		r02.meta['item'] = i
		yield r02
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
		price_id = j['pt_sp_address'].decode('utf8').split('/')[-1].split('.')[0]
		addserviceurl= 'http://d.jd.com/yanbao2/get?skuId=' + price_id + '&callback=jQuery6593076'
		r03 = Request(addserviceurl,callback=self.parseservice)
		r03.meta['item'] = j
		yield r03
	def parseservice(self,response):
		sel = Selector(text=response.body)
		try:
			service = eval(response.body.replace('null','""').replace('true','""').replace('jQuery6593076([','').replace('])',''))
			addservice = service[1]['sortName'] + " " + service[1]['price']

		except Exception,ex:
			print ex;
			addservice = ""
		item = response.meta['item']
		item['danpin_add_service'] = addservice

		return item
'''
