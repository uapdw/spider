# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime
from scrapy.exceptions import DropItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import pymongo
import hashlib
import time
import uuid
from items import NewMotorProductItem, NewMotorRateStastisticItem, NewMotorRateDetailItem, NewMotorRateStastisticItem, NewMotorProductDynamicItem
class BaiduNewsPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['baidu']:
	return item

      article = {"title":item['title'][0],'siteName':item['sitename'][0],'publishTime':item['publishtime'][0],'content':item['content'][0],'addTime':item['addtime'],'keyWords':item['keywords']}
      spider.tArticles.update({'url':item['url'][0]},{'$set':article},True)
      return item

class StockCompanyInfoPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['stockinfo']:
	return item
      print "enter StockCompanyInfoPipeline....."

      arrInfo = {}
      for i in item:
	if i == 'stockCode':
	  continue
	arrInfo[i] = item[i]

      spider.tCompanyInfo.update({'stockCode':item['stockCode']},{'$set':arrInfo},True)
      return item


class StockBalanceSheetPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['stockbalance']:
	return item
      print "enter StockBalanceSheetPipeline....."

      arrInfo = {}
      if u'科目'.encode('utf8') in item['row']:
	for i in item['row']:
	  if i == 'stockCode' or i == 'pubtime':
	    continue
	  arrInfo[i] = item['row'][i]

	spider.tBalanceSheet.update({'stockCode':item['row']['stockCode'],'pubtime':item['row']['pubtime']},{'$set':arrInfo},True)
	return item
      else:
	raise DropItem('No stock balance sheet datas in %s' % item)


class StockIncomeStatementsPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['stockincome']:
	return item
      print "enter StockIncomeStatementsPipeline....."

      arrInfo = {}
      if u'科目'.encode('utf8') in item['row']:
	for i in item['row']:
	  if i == 'stockCode' or i == 'pubtime':
	    continue
	  arrInfo[i] = item['row'][i]

	spider.tIncome.update({'stockCode':item['row']['stockCode'],'pubtime':item['row']['pubtime']},{'$set':arrInfo},True)
	return item
      else:
	raise DropItem('No stock income statements datas in %s' % item)

class StockCashFlowPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['stockcashflow']:
	return item
      print "enter StockCashFlowPipeline....."

      arrInfo = {}
      if u'科目'.encode('utf8') in item['row']:
	for i in item['row']:
	  if i == 'stockCode' or i == 'pubtime':
	    continue
	  arrInfo[i] = item['row'][i]

	spider.tCashFlow.update({'stockCode':item['row']['stockCode'],'pubtime':item['row']['pubtime']},{'$set':arrInfo},True)
	return item
      else:
	raise DropItem('No stock cash flow datas in %s' % item)

class StockFinancialReportPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['cninfo']:
	return item
      else:
	if item['iType'] == 'financialReport':
	  print "enter StockFinancialReportPipeline....."
	  print '='*10
	return item

class SteelIndexNumberPipeline(object):
  def process_item(self, item, spider):
    if spider.name not in ['steel']:
      return item

    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tSteelIndex = infoDB.steelindex

    print "enter SteelIndexNumberPipeline....."
    for index,pubDate in enumerate(item['pubDate']):
      data = {"indexnum":item['indexNumber'][index]}
      tSteelIndex.update({'pubdate':pubDate},{'$set':data},True)

    conn.close()
    return item

class StatsMacroIndexPipeline(object):
  def process_item(self, item, spider):
    if spider.name not in ['statsindex']:
      return item

    print "enter StatsMacroIndexPipeline....."
    data = {"name":item['name'],"parentcode":item['parentCode'],'ts':item['ts'],'ifdata':item['ifData'],'unit':item['unit'],'note':item['note']}
    spider.tMacroIndex.update({'code':item['code'],'period':item['period']},{'$set':data},True)
    return item

class StatsMacroDataPipeline(object):
  def process_item(self, item, spider):
    if spider.name not in ['statsdata']:
      return item

    print "enter StatsMacroDataPipeline....."

    if item['types'] == 'index':
      #print "Update index's unit....."
      indexItem = spider.tMacroIndex.find_one({'code':item['code'],'period':item['period']})
      indexItem['unit'] = item['unit']
      indexItem['note'] = item['note']
      spider.tMacroIndex.update({'_id':indexItem['_id']},indexItem)
    elif item['types'] == 'data':
      #print "Insert macro data....."
      data = {"code":item['code'],"name":item['name'],'area':item['area'],'ydate':item['ydate'],'qdate':item['qdate'],'mdate':item['mdate'],'value':item['value'],'desc':item['desc'],'ts':item['ts']}
      spider.tMacroData.update({'key':item['key']},{'$set':data},True)
    return item


class WhpjPipeline(object):
  def process_item(self, item, spider):
    if spider.name not in ['whpj']:
      return item

    print "enter WhpjPipeline....."
    t = datetime.datetime.strptime(item['releasetime'],'%Y.%m.%d %H:%M:%S')
    item['releasetime'] = t
    item['key'] = item['currentname'] + '_' + datetime.datetime.strftime(t,'%Y%m%d_%H%M%S')

    data = {'currentname':item['currentname'],'price_spot_in':item['price_spot_in'],'price_cash_in':item['price_cash_in'],'price_spot_out':item['price_spot_out'],'price_cash_out':item['price_cash_out'],'midprice':item['midprice'],'bocprice':item['bocprice'],'releasetime':item['releasetime'],'note':item['note'],'ts':item['ts']}
    spider.tWhpjRate.update({'key':item['key']},{'$set':data},True)
    #spider.tWhpjRate.insert(data)
    return item

class WebArticlePipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['jinghua','newshexun','qudong','sciencechina','yesky','pcpop','gmw','cctime','csdn','it168','chinabyte','zdnet','iresearchNews','dsj','techweb','dataguru','huxiu','chinaCloud','yidonghua','cbinews','ceocio','ctocio','chinacloud','chinamobile','leiphone','ctociocn','199it','sina','tech163','techqq','ifeng','sohu','net_baidu','ciotimes','ccidnet','donews','baidubaijia','cnddr','itbear','itpub','ynet','yos','zol']:
      return item

    print "enter WebArticlePipeLine...."
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    #elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
    #  raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
    else:
      data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
      spider.tWebArticles.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='other_articles:url',value=item['url']))
      mutations.append(Mutation(column='other_articles:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:publishTime',value=item['publishTime']))
      mutations.append(Mutation(column='other_articles:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:siteName',value=item['siteName']))
      mutations.append(Mutation(column='other_articles:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='other_articles:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      spider.client.mutateRow('info_public_monitor',row,mutations,None)
      return item

class WebBlogPipeLine(object):
  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)
  def __del__(self):
    self.transport.close()

  def process_item(self, item, spider):
    if spider.name not in ['iteye']:
      return item

    print "enter WebBlogPipeLine...."
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no blog item! @@@url=%s" % item['url'])
    elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
      raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
    else:
      data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
      spider.tWebBlogs.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='blog:url',value=item['url']))
      mutations.append(Mutation(column='blog:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='blog:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='blog:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='blog:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='blog:publishTime',value=item['publishTime']))
      mutations.append(Mutation(column='blog:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='blog:siteName',value=item['siteName']))
      mutations.append(Mutation(column='blog:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='blog:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      self.client.mutateRow('info_public_monitor',row,mutations,None)
      return item

class IndustryReportPipeLine(object):
  def process_item(self, item, spider):
		if spider.name not in ['idc','gartner','iresearchReport','eguan']:
			return item
		
		print "enter IndustryReportPipeLine...."
		yesterday = datetime.date.today() - datetime.timedelta(days=1)
		if item['title'] == '' or item['content'] == '':
			raise DropItem("there is no report item! @@@url=%s" % item['url'])
		#elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
		#	raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
		else:
			data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
			spider.tIndustryReport.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
			
			row = hashlib.new("md5",item['url']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='report:url',value=item['url']))
			mutations.append(Mutation(column='report:title',value=item['title'].encode("utf8")))
			mutations.append(Mutation(column='report:author',value=item['author'].encode("utf8")))
			mutations.append(Mutation(column='report:abstract',value=item['abstract'].encode("utf8")))
			mutations.append(Mutation(column='report:keyWords',value=item['keyWords'].encode("utf8")))
			mutations.append(Mutation(column='report:publishTime',value=item['publishTime']))
			mutations.append(Mutation(column='report:content',value=item['content'].encode("utf8")))
			mutations.append(Mutation(column='report:siteName',value=item['siteName']))
			mutations.append(Mutation(column='report:source',value=item['source'].encode("utf8")))
			mutations.append(Mutation(column='report:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
			spider.client.mutateRow('info_public_monitor',row,mutations,None)
			
			return item

class WebActivityPipeLine(object):
  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)
  def __del__(self):
    self.transport.close()

  def process_item(self, item, spider):
    if spider.name not in ['csdnactivity']:
      return item

    print "enter WebActivityPipeLine...."
    if item['title'] == '' or item['activityID'] == '':
      raise DropItem("there is no activity item! @@@url=%s" % item['url'])
    else:
      data = {'title':item['title'],'trad':item['trad'],'time':item['time'],'location':item['location'],'keyWords':item['keyWords'],'activityID':item['activityID'],'siteName':item['siteName'],'addTime':item['addTime']}
      spider.tWebActivity.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='activity:url',value=item['url']))
      mutations.append(Mutation(column='activity:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='activity:trad',value=item['trad'].encode("utf8")))
      mutations.append(Mutation(column='activity:time',value=item['time'].encode("utf8")))
      mutations.append(Mutation(column='activity:location',value=item['location'].encode("utf8")))
      mutations.append(Mutation(column='activity:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='activity:activityID',value=item['activityID']))
      mutations.append(Mutation(column='activity:siteName',value=item['siteName']))
      mutations.append(Mutation(column='activity:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      self.client.mutateRow('info_public_monitor',row,mutations,None)
      return item

class DianPingShopPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
	
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['DianpingShop']:
			return item
		print "enter DianPingShopPipeLine...."
		'''
    data = {'level':item['level'],'consume':item['consume'],'comment':item['comment'],'taste':item['taste'],'environment':item['environment'],'service':item['service'],'shopname':item['shopname'],'city':item['city'],'address':item['address'],'business':item['business']}
    spider.tDazhongdp.update({'shopid':item['shopid']},{'$set':data},True)
		'''
    #insert item into hbase
		row = hashlib.new("md5",item['shopid']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:shopid',value=item['shopid'].encode("utf8")))
		mutations.append(Mutation(column='column:shopname',value=item['shopname'].encode("utf8")))
		mutations.append(Mutation(column='column:city',value=item['city'].encode("utf8")))
		mutations.append(Mutation(column='column:address',value=item['address'].encode("utf8")))
		mutations.append(Mutation(column='column:business',value=item['business'].encode("utf8")))
		self.client.mutateRow('dianping_shop',row,mutations,None)
		
		mutations = []
		mutations.append(Mutation(column='column:shopid',value=item['shopid'].encode("utf8")))
		mutations.append(Mutation(column='column:level',value=item['level'].encode("utf8")))
		mutations.append(Mutation(column='column:consume',value=item['consume'].encode("utf8")))
		mutations.append(Mutation(column='column:comment',value=item['comment'].encode("utf8")))
		mutations.append(Mutation(column='column:taste',value=item['taste'].encode("utf8")))
		mutations.append(Mutation(column='column:environment',value=item['environment']))
		mutations.append(Mutation(column='column:service',value=item['service'].encode("utf8")))
		self.client.mutateRow('dianping_content',row,mutations,None)
		return item

class DianPingDishPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
	
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['DianpingDish']:
			return item
		print "enter DianPingDishPipeLine...."
		'''
    data = {'level':item['level'],'consume':item['consume'],'comment':item['comment'],'taste':item['taste'],'environment':item['environment'],'service':item['service'],'shopname':item['shopname'],'city':item['city'],'address':item['address'],'business':item['business']}
    spider.tDazhongdp.update({'shopid':item['shopid']},{'$set':data},True)
		'''
    #insert item into hbase
		j=0
		mutations = []
		if len(item['arrDish']) < 1:
			raise DropItem('No Dianping Dish datas in %s' % item)
		else:
			for i in item['arrDish']:
				if len(i) > 0:
					arrDish = i.split(',')
					row = item['shopid'] + "_" + str(j)
					mutations.append(Mutation(column='column:shopid',value=item['shopid'].encode("utf8")))
					mutations.append(Mutation(column='column:recommend',value=(arrDish[0]).encode("utf8")))
					mutations.append(Mutation(column='column:rnumber',value=(arrDish[1]).encode("utf8")))
					self.client.mutateRow('dianping_recommond',row,mutations,None)
					j+=1
		return item

class DaniangNewsPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
		
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['Yonghe','Yos','DnsjBaiDu','Mcdonalds','KFC','Cnddr']:
			return item
		
		print "enter DemoPipeLine...."
		#print item['title']
		if item['title'] == '':
			raise DropItem("there is no activity item! @@@url=%s" % item['url'])
		else:
			data = {'title':item['title'],'time':item['time'],'siteName':item['siteName']}
			spider.tDnsjNews.update({'url':item['url']},{'$set':data},True)
			'''
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='activity:url',value=item['url']))
      mutations.append(Mutation(column='activity:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='activity:trad',value=item['trad'].encode("utf8")))
      mutations.append(Mutation(column='activity:time',value=item['time'].encode("utf8")))
      mutations.append(Mutation(column='activity:location',value=item['location'].encode("utf8")))
      mutations.append(Mutation(column='activity:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='activity:activityID',value=item['activityID']))
      mutations.append(Mutation(column='activity:siteName',value=item['siteName']))
      mutations.append(Mutation(column='activity:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      self.client.mutateRow('',row,mutations,None)
			'''
			return item

class DaniangWeiBoPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
		
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['DnWeiBo']:
			return item
		
		print "enter DemoPipeLine...."
		#print item['userurl']
		if item['time'] == '':
			raise DropItem("there is no activity item! @@@url=%s" % item['weibourl'])
		else:
			data = {'username':item['username'],'userurl':item['userurl'],'image':item['image'],'content':item['content'],'source':item['source'],'time':item['time']}
			spider.tDnsjWeiBo.update({'weibourl':item['weibourl']},{'$set':data},True)
			'''
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='activity:url',value=item['url']))
      mutations.append(Mutation(column='activity:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='activity:trad',value=item['trad'].encode("utf8")))
      mutations.append(Mutation(column='activity:time',value=item['time'].encode("utf8")))
      mutations.append(Mutation(column='activity:location',value=item['location'].encode("utf8")))
      mutations.append(Mutation(column='activity:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='activity:activityID',value=item['activityID']))
      mutations.append(Mutation(column='activity:siteName',value=item['siteName']))
      mutations.append(Mutation(column='activity:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      self.client.mutateRow('',row,mutations,None)
			'''
			return item
class DaniangWeiXinPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
		
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['DnsjWeiXin']:
			return item
		
		print "enter WeiXinPipeLine...."
		#print item['title']
		if item['title'] == '':
			raise DropItem("there is no activity item! @@@url=%s" % item['url'])
		else:
			data = {'title':item['title'],'time':item['time'],'content':item['content'],'source':item['source'],'image':item['image']}
			spider.tDnsjWeiXin.update({'url':item['url']},{'$set':data},True)
			'''
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='activity:url',value=item['url']))
      mutations.append(Mutation(column='activity:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='activity:trad',value=item['trad'].encode("utf8")))
      mutations.append(Mutation(column='activity:time',value=item['time'].encode("utf8")))
      mutations.append(Mutation(column='activity:location',value=item['location'].encode("utf8")))
      mutations.append(Mutation(column='activity:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='activity:activityID',value=item['activityID']))
      mutations.append(Mutation(column='activity:siteName',value=item['siteName']))
      mutations.append(Mutation(column='activity:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      self.client.mutateRow('',row,mutations,None)
			'''
			return item
class GovSubPipeLine(object):
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
	
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['GovSub']:
			return item
		print "enter GovSubPipeLine...."
		'''
    data = {'level':item['level'],'consume':item['consume'],'comment':item['comment'],'taste':item['taste'],'environment':item['environment'],'service':item['service'],'shopname':item['shopname'],'city':item['city'],'address':item['address'],'business':item['business']}
    spider.tDazhongdp.update({'shopid':item['shopid']},{'$set':data},True)
		'''
    #insert item into hbase
		
		row = hashlib.new("md5",item['url']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:url',value=item['url']))
		mutations.append(Mutation(column='column:title',value=item['title'].encode("utf8")))
		mutations.append(Mutation(column='column:buyer',value=item['buyer'].encode("utf8")))
		mutations.append(Mutation(column='column:agent',value=item['agent'].encode("utf8")))
		mutations.append(Mutation(column='column:abstract',value=item['abstract'].encode("utf8")))
		mutations.append(Mutation(column='column:keyWords',value=item['keyWords'].encode("utf8")))
		mutations.append(Mutation(column='column:publishTime',value=item['publishTime'].encode("utf8")))
		mutations.append(Mutation(column='column:content',value=item['content'].encode("utf8")))
		mutations.append(Mutation(column='column:source',value=item['source']))
		self.client.mutateRow('china_govsub',row,mutations,None)
		
		
		return item
class JDBaseInfoPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['JDBaseInfo']:
			return item
		print "enter JDBaseInfoPipeLine...."
		
		data = {'shopurl':item['shopurl'],'shopid':item['shopid']}
		spider.tJDBaseInfo.update({'shopurl':item['shopurl']},{'$set':data},True)
		'''
		#insert item into hbase
		
		row = hashlib.new("md5",item['url']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:url',value=item['url']))
		mutations.append(Mutation(column='column:title',value=item['title'].encode("utf8")))
		mutations.append(Mutation(column='column:buyer',value=item['buyer'].encode("utf8")))
		mutations.append(Mutation(column='column:agent',value=item['agent'].encode("utf8")))
		mutations.append(Mutation(column='column:abstract',value=item['abstract'].encode("utf8")))
		mutations.append(Mutation(column='column:keyWords',value=item['keyWords'].encode("utf8")))
		mutations.append(Mutation(column='column:publishTime',value=item['publishTime'].encode("utf8")))
		mutations.append(Mutation(column='column:content',value=item['content'].encode("utf8")))
		mutations.append(Mutation(column='column:source',value=item['source']))
		self.client.mutateRow('china_govsub',row,mutations,None)
		
		'''
		return item
class JDCommDetailPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['JDCommDetail']:
			return item
		print "enter JdCommDetailPipeLine...."
		
		#data = {'pt_name':item['ptname'],'danpin_name':item['danpinname'],'pt_sp_address':item['ptspaddress'],'satisfaction':item['satisfaction'],'com_keywords':item['comkeywords'],'com_feel_up':item['com_feel_up'],'com_feel':item['comfeel'],'com_order_show':item['comordershow'],'com_feel_reply':item['comfeelreply'],'com_establish_time':item['comestablishtime'],'order_buy_info':item['orderbuyinfo'],'com_id':item['comid'],'com_id_level':item['comidlevel'],'com_id_address':item['comidaddress'],'order_buy_time':item['orderbuytime']}
		
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
		
    #insert item into hbase
		
		row = hashlib.new("md5",'JD'+item['comestablishtime']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:pt_sp_address',value=item['ptspaddress']))
		mutations.append(Mutation(column='column:pt_name',value=item['ptname'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_name',value=item['danpinname'].encode("utf8")))
		mutations.append(Mutation(column='column:satisfaction',value=item['satisfaction'].encode("utf8")))
		mutations.append(Mutation(column='column:com_keywords',value=item['comkeywords'].encode("utf8")))
		mutations.append(Mutation(column='column:com_feel',value=item['comfeel'].encode("utf8")))
		mutations.append(Mutation(column='column:com_order_show',value=item['comordershow'].encode("utf8")))
		mutations.append(Mutation(column='column:com_feel_reply',value=item['comfeelreply'].encode("utf8")))
		mutations.append(Mutation(column='column:com_establish_time',value=item['comestablishtime'].encode("utf8")))
		mutations.append(Mutation(column='column:order_buy_info',value=item['orderbuyinfo'].encode("utf8")))
		mutations.append(Mutation(column='column:com_id',value=item['comid'].encode("utf8")))
		mutations.append(Mutation(column='column:com_id_level',value=item['comidlevel'].encode("utf8")))
		mutations.append(Mutation(column='column:com_feel_up',value=item['com_feel_up'].encode("utf8")))
		mutations.append(Mutation(column='column:com_id_address',value=item['comidaddress'].encode("utf8")))
		mutations.append(Mutation(column='column:order_buy_time',value=item['orderbuytime'].encode("utf8")))
		mutations.append(Mutation(column='column:sentiment',value=''))
		#spider.client.mutateRow('DS_DETAIL_COM',row,mutations,None)
		spider.client.mutateRow('spider_ds_detail_com',row,mutations,None)
		
		
		'''
		if item['com_reply_name']:
			for key in range(len(item['com_reply_name'])-1):
				mutations1 = []
				row01 = hashlib.new("md5",item['com_reply_addtime'][key].encode("utf8")).hexdigest()
				mutations1.append(Mutation(column='column:com_id',value=item['comid'].encode("utf8")))
				mutations1.append(Mutation(column='column:com_reply_name',value=item['com_reply_name'][key].encode("utf8")))
				mutations1.append(Mutation(column='column:com_reply_addtime',value=item['com_reply_addtime'][key].encode("utf8")))
				mutations1.append(Mutation(column='column:com_reply_content',value=item['com_reply_content'][key].encode("utf8")))
				self.client.mutateRow('DS_DETAIL_REPLY',row01,mutations1,None)
		'''

		return item

class JDWaresInfoPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['JDWaresInfo','JDWaresInfoTest','SNDSSPInfo']:
			return item
		print "enter JDWaresInfoPipeLine...."
		
		#data = {'pt_name':item['pt_name'],'pt_sp_address':item['pt_sp_address'],'danpin_promotion':item['danpin_promotion'],'danpin_carrier':item['danpin_carrier'],'name':item['name'],'pinlei':item['pinlei'],'dalei':item['dalei'],'xiaolei':item['xiaolei'],'brand':item['brand'],'danpin_name':item['danpin_name'],'danpin_code':item['danpin_code'],'danpin_photo':item['danpin_photo'],'danpin_intro':item['danpin_intro'],'danpin_spec':item['danpin_spec'],'danpin_package':item['danpin_package'],'danpin_after_sale':item['danpin_after_sale'],'danpin_slogan':item['danpin_slogan'],'danpin_info_detail':item['danpin_info_detail'],'danpin_price':item['danpin_price'],'danpin_fare':item['danpin_fare'],'danpin_payment_method':item['danpin_payment_method'],'danpin_add_service':item['danpin_add_service'],'danpin_service_tips':item['danpin_service_tips']}
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
    #insert item into hbase
		print item

		row = hashlib.new("md5",item['pt_sp_address']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address'].encode("utf8")))
		mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
		mutations.append(Mutation(column='column:name',value=item['name'].encode("utf8")))
		mutations.append(Mutation(column='column:pinlei',value=item['pinlei'].encode("utf8")))
		mutations.append(Mutation(column='column:dalei',value=item['dalei'].encode("utf8")))
		mutations.append(Mutation(column='column:xiaolei',value=item['xiaolei'].encode("utf8")))
		mutations.append(Mutation(column='column:brand',value=item['brand'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_code',value=item['danpin_code'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_photo',value=item['danpin_photo'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_intro',value=item['danpin_intro'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_spec',value=item['danpin_spec'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_package',value=item['danpin_package'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_after_sale',value=item['danpin_after_sale'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_slogan',value=item['danpin_slogan'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_info_detail',value=item['danpin_info_detail'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_price',value=item['danpin_price']))
		mutations.append(Mutation(column='column:danpin_promotion',value=item['danpin_promotion'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_carrier',value=item['danpin_carrier'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_fare',value=item['danpin_fare'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_payment_method',value=item['danpin_payment_method'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_add_service',value=item['danpin_add_service'].encode("utf8")))
		#mutations.append(Mutation(column='column:danpin_credit_service',value=item['danpin_credit_service'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_service_tips',value=item['danpin_service_tips'].encode("utf8")))
		spider.client.mutateRow('DS_SPinfo',row,mutations,None)
		return item

class JDSummaryCommPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['JDSummaryComm']:
			return item
		print "enter JDSummaryCommPipeLine...."
		
		data = {'pt_name':item['pt_name'],'danpin_name':item['danpin_name'],'pt_sp_address':item['pt_sp_address'],'com_count':item['com_count'],'positive_com_count':item['positive_com_count'],'moderate_com_count':item['moderate_com_count'],'negative_com_count':item['negative_com_count'],'photo_com_count':item['photo_com_count'],'impression':item['impression']}
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
		
    #insert item into hbase
		
		row = hashlib.new("md5",item['pt_sp_address']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address']))
		mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
		mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
		mutations.append(Mutation(column='column:com_count',value=item['com_count'].encode("utf8")))
		mutations.append(Mutation(column='column:positive_com_count',value=item['positive_com_count'].encode("utf8")))
		mutations.append(Mutation(column='column:moderate_com_count',value=item['moderate_com_count'].encode("utf8")))
		mutations.append(Mutation(column='column:negative_com_count',value=item['negative_com_count'].encode("utf8")))
		mutations.append(Mutation(column='column:photo_com_count',value=item['photo_com_count'].encode("utf8")))
		mutations.append(Mutation(column='column:impression',value=item['impression'].encode("utf8")))
		spider.client.mutateRow('DS_TOTAL_COM',row,mutations,None)
		return item

class JDDpInfoTestPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['JDDpInfoTest']:
			return item
		print "enter JDDpInfoTestPipeLine...."
		
		data = {'pt_name':item['pt_name'],'name':item['name'],'score_total':item['score_total'],'sp_score':item['sp_score'],'sp_compare':item['sp_compare'],'service_score':item['service_score'],'service_compare':item['service_compare'],'eff_score':item['eff_score'],'eff_compare':item['eff_compare'],'Company_name':item['Company_name'],'Company_city':item['Company_city'],'Surport_service':item['Surport_service'],'service_inf':item['service_inf']}
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
		
    #insert item into hbase
		
		row = hashlib.new("md5",item['url']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:name',value=item['name'].encode("utf8")))
		mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
		mutations.append(Mutation(column='column:score_total',value=item['score_total'].encode("utf8")))
		mutations.append(Mutation(column='column:sp_score',value=item['sp_score'].encode("utf8")))
		mutations.append(Mutation(column='column:sp_compare',value=item['sp_compare'].encode("utf8")))
		mutations.append(Mutation(column='column:service_score',value=item['service_score'].encode("utf8")))
		mutations.append(Mutation(column='column:service_compare',value=item['service_compare'].encode("utf8")))
		mutations.append(Mutation(column='column:eff_score',value=item['eff_score'].encode("utf8")))
		mutations.append(Mutation(column='column:eff_compare',value=item['eff_compare'].encode("utf8")))
		mutations.append(Mutation(column='column:Company_name',value=item['Company_name'].encode("utf8")))
		mutations.append(Mutation(column='column:Company_city',value=item['Company_city'].encode("utf8")))
		mutations.append(Mutation(column='column:Surport_service',value=item['Surport_service'].encode("utf8")))
		mutations.append(Mutation(column='column:service_inf',value=item['service_inf'].encode("utf8")))
		spider.client.mutateRow('DS_DPinfo',row,mutations,None)
		return item

class HRDataPipeLine(object):
	def __init__(self):
		#self.host = "172.20.8.69"
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
	
	def __del__(self):
		self.transport.close()
		
	def process_item(self, item, spider):
		if spider.name not in ['HRDataZhiL','HRDataYinC','Job51JobSpider']:
			return item
		print "enter HRDataPipeLine...."
		
		#data = {'pt_name':item['pt_name'],'pt_sp_address':item['pt_sp_address'],'danpin_promotion':item['danpin_promotion'],'danpin_carrier':item['danpin_carrier'],'name':item['name'],'pinlei':item['pinlei'],'dalei':item['dalei'],'xiaolei':item['xiaolei'],'brand':item['brand'],'danpin_name':item['danpin_name'],'danpin_code':item['danpin_code'],'danpin_photo':item['danpin_photo'],'danpin_intro':item['danpin_intro'],'danpin_spec':item['danpin_spec'],'danpin_package':item['danpin_package'],'danpin_after_sale':item['danpin_after_sale'],'danpin_slogan':item['danpin_slogan'],'danpin_info_detail':item['danpin_info_detail'],'danpin_price':item['danpin_price'],'danpin_fare':item['danpin_fare'],'danpin_payment_method':item['danpin_payment_method'],'danpin_add_service':item['danpin_add_service'],'danpin_service_tips':item['danpin_service_tips']}
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
    #insert item into hbase
		
		
		row = hashlib.new("md5",item['url']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:name_company',value=item['name_company'].encode("utf8")))
		mutations.append(Mutation(column='column:web_source',value=item['websource'].encode("utf8")))
		mutations.append(Mutation(column='column:scale_company',value=item['scale_company'].encode("utf8")))
		mutations.append(Mutation(column='column:type_company',value=item['type_company'].encode("utf8")))
		mutations.append(Mutation(column='column:industry_company',value=item['industry_company'].encode("utf8")))
		mutations.append(Mutation(column='column:website_company',value=item['website_company'].encode("utf8")))
		mutations.append(Mutation(column='column:address_company',value=item['address_company'].encode("utf8")))
		mutations.append(Mutation(column='column:info_company',value=item['info_company'].encode("utf8")))
		mutations.append(Mutation(column='column:name_position',value=item['name_position'].encode("utf8")))
		mutations.append(Mutation(column='column:url',value=item['url'].encode("utf8")))
		mutations.append(Mutation(column='column:keywords_position',value=item['keywords_position'].encode("utf8")))
		mutations.append(Mutation(column='column:salary_position',value=item['salary_position'].encode("utf8")))
		mutations.append(Mutation(column='column:location_position',value=item['location_position'].encode("utf8")))
		mutations.append(Mutation(column='column:release_time',value=item['release_time'].strftime("%Y-%m-%d %H:%M:%S")))
		mutations.append(Mutation(column='column:nature_position',value=item['nature_position'].encode("utf8")))
		mutations.append(Mutation(column='column:experience_position',value=item['experience_position'].encode("utf8")))
		mutations.append(Mutation(column='column:education_demand',value=item['education_demand'].encode("utf8")))
		mutations.append(Mutation(column='column:sex_requrment',value=item['sex_requrment'].encode("utf8")))
		mutations.append(Mutation(column='column:number_demand',value=item['number_demand'].encode("utf8")))
		mutations.append(Mutation(column='column:type_position',value=item['type_position'].encode("utf8")))
		mutations.append(Mutation(column='column:jd_position',value=item['jd_position'].encode("utf8")))
		mutations.append(Mutation(column='column:sex_requrment',value=item['sex_requrment'].encode("utf8")))
		mutations.append(Mutation(column='column:duty_position',value=item['dutypos'].encode("utf8")))
		mutations.append(Mutation(column='column:requiremen_position',value=item['requiremen_position'].encode("utf8")))
		mutations.append(Mutation(column='column:pay_position',value=item['pay_position'].encode("utf8")))
		mutations.append(Mutation(column='column:welfare_position',value=item['welfare_position'].encode("utf8")))
		mutations.append(Mutation(column='column:name_contact',value=item['name_contact'].encode("utf8")))
		mutations.append(Mutation(column='column:tele_contact',value=item['tele_contact'].encode("utf8")))
		mutations.append(Mutation(column='column:email_contact',value=item['email_contact'].encode("utf8")))
		self.client.mutateRow('HR_Data',row,mutations,None)
		return item

class PM25ChinaPipeLine(object):
	'''
	def __init__(self):
		print '#' *40
		self.host = "172.20.8.69"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)
	
	def __del__(self):
		self.transport.close()
	'''
		
	def process_item(self, item, spider):
		if spider.name not in ['PM25China']:
			return item
		print "enter PM25ChinaPipeLine...."
		
		#data = {'pt_name':item['pt_name'],'name':item['name'],'score_total':item['score_total'],'sp_score':item['sp_score'],'sp_compare':item['sp_compare'],'service_score':item['service_score'],'service_compare':item['service_compare'],'eff_score':item['eff_score'],'eff_compare':item['eff_compare'],'Company_name':item['Company_name'],'Company_city':item['Company_city'],'Surport_service':item['Surport_service'],'service_inf':item['service_inf']}
		#spider.tJdCommDetail.update({'comid':item['comid']},{'$set':data},True)
		
    #insert item into hbase
		
		row = hashlib.new("md5",item['crawltime'] + item['jiankongdian_code']).hexdigest()
		
		mutations = []
		mutations.append(Mutation(column='column:areacode',value=item['areacode'].encode("utf8")))
		mutations.append(Mutation(column='column:areaname',value=item['areaname'].encode("utf8")+'市'))
		mutations.append(Mutation(column='column:publishtime',value=item['publishtime'].encode("utf8")))
		mutations.append(Mutation(column='column:index_value',value=item['index_value'].encode("utf8")))
		mutations.append(Mutation(column='column:jiankongdian_code',value=item['jiankongdian_code'].encode("utf8")))
		mutations.append(Mutation(column='column:jiankongdian_name',value=item['jiankongdian_name'].encode("utf8")))
		mutations.append(Mutation(column='column:jiangkongdian_aqi',value=item['jiangkongdian_aqi'].encode("utf8")))
		mutations.append(Mutation(column='column:jiangkongdian_pm25',value=item['jiangkongdian_pm25'].encode("utf8")))
		mutations.append(Mutation(column='column:jiangkongdian_pm10',value=item['jiangkongdian_pm10'].encode("utf8")))
		mutations.append(Mutation(column='column:jiangkongdian_key',value=item['jiangkongdian_key'].encode("utf8")))
		mutations.append(Mutation(column='column:crawltime',value=item['crawltime'].encode("utf8")))
		spider.client.mutateRow('dw_pm25',row,mutations,None)
		return item

class PublicDemoArticlePipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['abi','cena','ea3w','hc360','hea163','newscheaa','smarthomeqianjia']:
      return item

    print "enter PublicDemoArticlePipeLine...."
    #print "item num is : %d" % len(spider.itemList)
    print "*"*50

    '''
    if len(spider.itemList) == 100:
      print "batch insert into HBase...."
      mutationsBatch = []
      for i in spider.itemList:
        if i['title'] == '' or i['content'] == '':
          pass
          #raise DropItem("there is no article item! @@@url=%s" % item['url'])
        else:
          row = hashlib.new("md5",i['url']).hexdigest()
          mutations = []
          mutations.append(Mutation(column='article:url',value=i['url']))
          mutations.append(Mutation(column='article:title',value=i['title'].encode("utf8")))
          mutations.append(Mutation(column='article:author',value=i['author'].encode("utf8")))
          mutations.append(Mutation(column='article:abstract',value=i['abstract'].encode("utf8")))
          mutations.append(Mutation(column='article:keyWords',value=i['keyWords'].encode("utf8")))
          mutations.append(Mutation(column='article:publishTime',value=i['publishTime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
          mutations.append(Mutation(column='article:content',value=i['content'].encode("utf8")))
          mutations.append(Mutation(column='article:siteName',value=i['siteName'].encode("utf8")))
          mutations.append(Mutation(column='article:source',value=i['source'].encode("utf8")))
          mutations.append(Mutation(column='article:addTime',value=i['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
          mutations.append(Mutation(column='article:sentiment',value=''))
          #spider.client.mutateRow('spider_info_public_demo',row,mutations,None)
          mutationsBatch.append(BatchMutation(row=row,mutations=mutations))

      spider.client.mutateRows('spider_info_public_demo',mutationsBatch,None)
      del spider.itemList[0:len(spider.itemList)]
    '''
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    #elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
    #  raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
    else:
      #data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
      #spider.tWebArticles.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='article:url',value=item['url']))
      mutations.append(Mutation(column='article:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='article:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='article:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='article:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='article:newstype',value=item['newstype'].encode("utf8")))
      mutations.append(Mutation(column='article:publishTime',value=item['publishTime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
      mutations.append(Mutation(column='article:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='article:siteName',value=item['siteName'].encode("utf8")))
      mutations.append(Mutation(column='article:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='article:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      mutations.append(Mutation(column='article:sentiment',value=''))
      spider.client.mutateRow('spider_info_public_demo',row,mutations,None)

    return item

class PublicDemoBBSPipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['baisejiadiantieba','bbscheaa','jdbbs','jdwxinfo']:
      return item

    print "enter PublicDemoBBSPipeLine...."
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    #elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
    #  raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
    else:
      #data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
      #spider.tWebArticles.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='bbs:url',value=item['url']))
      mutations.append(Mutation(column='bbs:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='bbs:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='bbs:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='bbs:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='bbs:publishTime',value=item['publishTime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
      mutations.append(Mutation(column='bbs:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='bbs:siteName',value=item['siteName'].encode("utf8")))
      mutations.append(Mutation(column='bbs:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='bbs:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      mutations.append(Mutation(column='bbs:sentiment',value=''))
      spider.client.mutateRow('spider_info_public_demo',row,mutations,None)
      return item

class PublicDemoBBSNewPipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['zongshen_autohome','zongshen_bbsmoto8','zongshen_motorfans','zongshen_newmotor','zongshen_tieba','zongshen_zongshenmotor']:
      return item

    print "enter PublicDemoBBSNewPipeLine...."
    if item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    else:
      row = hashlib.new("md5",item['siteName'] + '_' + item['threadId'] + '_' + item['postId']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='bbsnew:url',value=item['url']))
      mutations.append(Mutation(column='bbsnew:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:threadId',value=item['threadId'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:postId',value=item['postId'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:publishTime',value=item['publishTime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
      mutations.append(Mutation(column='bbsnew:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:siteName',value=item['siteName'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='bbsnew:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      mutations.append(Mutation(column='bbsnew:sentiment',value=''))
      spider.client.mutateRow('spider_info_public_demo',row,mutations,None)
      return item
class PublicDemoArticleNewPipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['chmotor','newmotor','zongs_weixin','zongs_baidu','zongs_hexun','zongs_caijing','zongs_caam','zongshen_haojue','zongshen_lifan','zongshen_wuyanghonda','zongshen_zongshencc']:
      return item

    print "enter PublicDemoArticlePipeLine...."
    #print "item num is : %d" % len(spider.itemList)
    print "*"*50

    print item
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    #elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
    #  raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
    else:
      #data = {'title':item['title'],'author':item['author'],'abstract':item['abstract'],'keyWords':item['keyWords'],'publishTime':item['publishTime'],'content':item['content'],'siteName':item['siteName'],'source':item['source'],'addTime':item['addTime']}
      #spider.tWebArticles.update({'url':item['url']},{'$set':data},True)
      #insert item into hbase
    
      row = hashlib.new("md5",item['url']).hexdigest()
      mutations = []
      mutations.append(Mutation(column='article:url',value=item['url']))
      mutations.append(Mutation(column='article:title',value=item['title'].encode("utf8")))
      mutations.append(Mutation(column='article:author',value=item['author'].encode("utf8")))
      mutations.append(Mutation(column='article:abstract',value=item['abstract'].encode("utf8")))
      mutations.append(Mutation(column='article:keyWords',value=item['keyWords'].encode("utf8")))
      mutations.append(Mutation(column='article:publishTime',value=item['publishTime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
      mutations.append(Mutation(column='article:content',value=item['content'].encode("utf8")))
      mutations.append(Mutation(column='article:siteName',value=item['siteName'].encode("utf8")))
      mutations.append(Mutation(column='article:source',value=item['source'].encode("utf8")))
      mutations.append(Mutation(column='article:newstype',value=item['newstype']))
      mutations.append(Mutation(column='article:addTime',value=item['addTime'].strftime("%Y-%m-%d %H:%M:%S")))
      mutations.append(Mutation(column='article:sentiment',value=''))
      spider.client.mutateRow('spider_info_public_demo',row,mutations,None)
      return item
   

class NewMotorPipeLine(object):
	def process_item(self, item, spider):
		if spider.name not in ['zongshen_mallnewmotor']:
			return item
		print "enter NewMotorPipeLine...."
		
		print item.__class__.__name__

		if isinstance(item, NewMotorProductItem):
			print "processing NewMotorProductItem...."
			row = hashlib.new("md5",item['pt_sp_address']).hexdigest()
		
			mutations = []
			mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address'].encode("utf8")))
			mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
			mutations.append(Mutation(column='column:name',value=item['name'].encode("utf8")))
			mutations.append(Mutation(column='column:pinlei',value=item['pinlei'].encode("utf8")))
			mutations.append(Mutation(column='column:dalei',value=item['dalei'].encode("utf8")))
			mutations.append(Mutation(column='column:xiaolei',value=item['xiaolei'].encode("utf8")))
			mutations.append(Mutation(column='column:brand',value=item['brand'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_longname',value=item['danpin_longname'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_code',value=item['danpin_code'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_photo',value=item['danpin_photo'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_intro',value=item['danpin_intro'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_spec',value=item['danpin_spec'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_package',value=item['danpin_package'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_slogan',value=item['danpin_slogan'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_price',value=item['danpin_price'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_stock',value=item['danpin_stock'].encode("utf8")))	
			mutations.append(Mutation(column='column:danpin_service_tips',value=item['danpin_service_tips'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_sale',value=item['danpin_sale'].encode("utf8")))

			mutations.append(Mutation(column='column:fuel_economy',value=item['fuel_economy'].encode("utf8")))
			mutations.append(Mutation(column='column:full_weight',value=item['full_weight'].encode("utf8")))
			mutations.append(Mutation(column='column:cylinders_count',value=item['cylinders_count'].encode("utf8")))
			mutations.append(Mutation(column='column:rim',value=item['rim'].encode("utf8")))
			mutations.append(Mutation(column='column:fuel_capacity',value=item['fuel_capacity'].encode("utf8")))
			mutations.append(Mutation(column='column:maximum_torque',value=item['maximum_torque'].encode("utf8")))
			mutations.append(Mutation(column='column:clearance',value=item['clearance'].encode("utf8")))
			mutations.append(Mutation(column='column:cooling',value=item['cooling'].encode("utf8")))
			mutations.append(Mutation(column='column:brake',value=item['brake'].encode("utf8")))
			mutations.append(Mutation(column='column:rear_wheel_size',value=item['rear_wheel_size'].encode("utf8")))
			mutations.append(Mutation(column='column:environmental_standards',value=item['environmental_standards'].encode("utf8")))
			mutations.append(Mutation(column='column:wheel_count',value=item['wheel_count'].encode("utf8")))
			mutations.append(Mutation(column='column:compression_ratio',value=item['compression_ratio'].encode("utf8")))
			mutations.append(Mutation(column='column:oil_supply',value=item['oil_supply'].encode("utf8")))
			mutations.append(Mutation(column='column:top_speed',value=item['top_speed'].encode("utf8")))
			mutations.append(Mutation(column='column:clutch',value=item['clutch'].encode("utf8")))
			mutations.append(Mutation(column='column:stroke',value=item['stroke'].encode("utf8")))
			mutations.append(Mutation(column='column:release_time',value=item['release_time'].strftime("%Y-%m-%d %H:%M:%S")))
			mutations.append(Mutation(column='column:available_colors',value=item['available_colors'].encode("utf8")))
			mutations.append(Mutation(column='column:empty_weight',value=item['empty_weight'].encode("utf8")))
			mutations.append(Mutation(column='column:transmission_type',value=item['transmission_type'].encode("utf8")))
			mutations.append(Mutation(column='column:engine_displacement',value=item['engine_displacement'].encode("utf8")))
			mutations.append(Mutation(column='column:wheelbase',value=item['wheelbase'].encode("utf8")))
			mutations.append(Mutation(column='column:seat_height',value=item['seat_height'].encode("utf8")))
			mutations.append(Mutation(column='column:size',value=item['size'].encode("utf8")))
			mutations.append(Mutation(column='column:production_status',value=item['production_status'].encode("utf8")))
			mutations.append(Mutation(column='column:starting_method',value=item['starting_method'].encode("utf8")))
			mutations.append(Mutation(column='column:front_wheel_size',value=item['front_wheel_size'].encode("utf8")))
			mutations.append(Mutation(column='column:maximum_power',value=item['maximum_power'].encode("utf8")))
			spider.client.mutateRow('ds_motor_danpin',row,mutations,None)
		
		elif isinstance(item,NewMotorProductDynamicItem):
			print "processing NewMotorProductDynamicItem...."
			row = hashlib.new("md5",item['pt_sp_address'] + item['crawl_time'].strftime("%Y-%m-%d %H:%M:%S")).hexdigest()
		
			mutations = []
			mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address'].encode("utf8")))
			mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
			mutations.append(Mutation(column='column:crawl_time',value=item['crawl_time'].strftime("%Y-%m-%d %H:%M:%S")))
			mutations.append(Mutation(column='column:danpin_sale',value=item['danpin_sale'].encode("utf8")))	
			mutations.append(Mutation(column='column:danpin_price',value=item['danpin_price'].encode("utf8")))
			spider.client.mutateRow('ds_motor_danpin_dynamic',row,mutations,None)

		elif isinstance(item,NewMotorRateStastisticItem):
			print "processing NewMotorRateStastisticItem...."
			row = hashlib.new("md5",item['pt_sp_address']).hexdigest()
		
			mutations = []
			mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address'].encode("utf8")))
			mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
			mutations.append(Mutation(column='column:com_count',value=item['com_count'].encode("utf8")))
			mutations.append(Mutation(column='column:positive_com_count',value=item['positive_com_count'].encode("utf8")))	
			mutations.append(Mutation(column='column:moderate_com_count',value=item['moderate_com_count'].encode("utf8")))
			mutations.append(Mutation(column='column:negative_com_count',value=item['negative_com_count'].encode("utf8")))
			spider.client.mutateRow('ds_motor_com_total',row,mutations,None)

		elif isinstance(item,NewMotorRateDetailItem):
			print "processing NewMotorRateDetailItem...."
			row = hashlib.new("md5",item['pt_sp_address'] + '_' + item['com_id'].encode("utf8") + '_' + item['com_establish_time'].strftime("%Y-%m-%d %H:%M:%S")).hexdigest()
		
			mutations = []
			mutations.append(Mutation(column='column:pt_sp_address',value=item['pt_sp_address'].encode("utf8")))
			mutations.append(Mutation(column='column:pt_name',value=item['pt_name'].encode("utf8")))
			mutations.append(Mutation(column='column:danpin_name',value=item['danpin_name'].encode("utf8")))
			mutations.append(Mutation(column='column:com_feel',value=item['com_feel'].encode("utf8")))
			mutations.append(Mutation(column='column:com_id',value=item['com_id'].encode("utf8")))	
			mutations.append(Mutation(column='column:com_establish_time',value=item['com_establish_time'].strftime("%Y-%m-%d %H:%M:%S")))
			spider.client.mutateRow('spider_ds_motor_com_detail',row,mutations,None)

