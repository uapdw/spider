# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider
from infomation_crawler.items import DianPingDishItem
from scrapy.exceptions import DropItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import json
import pymongo
import hashlib
import re

class DianpingDishSpider(Spider):
	def getHBaseList(tablename,cloum):
		host = "172.20.6.61"
		port = 9090
		transport = TBufferedTransport(TSocket(host,port))
		transport.open()
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		client = Hbase.Client(protocol)
		scanner = client.scannerOpen(tablename,'',cloum,None)
		res = client.scannerGetList(scanner,100000)
		client.scannerClose(scanner)
		return res
	name = 'DianpingDish'
	allowed_domain = ['dianping.com']
	urls = []
	temp = getHBaseList('dianping_shop',['column:shopid'])
	for i in temp:
		urls.append(
				'http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP?_nr_force=1421730900352&shopId=%s' % i.columns.get('column:shopid').value
				)
	start_urls = urls

	def parse(self, response):
		dish_data = []
		dish_count = []
		re_d=re.compile(r'shopId*')
		json_data = json.loads(response.body)
		dishTags = json_data['msg']['shopInfo']['dishTags']
		if dishTags == '' or dishTags == None:
			arrDish = []
		else:
			arrDish = dishTags.split('|')

		i = DianPingDishItem()
		i['shopid'] = ((response.url).split('&')[1]).split('=')[1]
		i['arrDish'] = arrDish
		return i
