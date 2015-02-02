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
    if spider.name not in ['csdn','it168','chinabyte','zdnet','iresearchNews','dsj','techweb','dataguru','huxiu','chinaCloud','yidonghua','cbinews','ceocio','ctocio','chinamobile','leiphone','ctocioCN','199it','sina','tech163','techqq','ifeng','sohu','net_baidu','ciotimes','ccidnet','donews']:
      return item

    print "enter WebArticlePipeLine...."
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item! @@@url=%s" % item['url'])
    elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
      raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
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
      self.client.mutateRow('info_public_monitor',row,mutations,None)
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
    if spider.name not in ['idc','gartner','iresearchReport','eguan']:
      return item

    print "enter IndustryReportPipeLine...."
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no report item! @@@url=%s" % item['url'])
    elif cmp(item['publishTime'],str(yesterday))!=0 and cmp(item['publishTime'],str(datetime.date.today()))!=0:
      raise DropItem("the article is not fresh! @@@publishTime=%s, url=%s" % (item['publishTime'],item['url']))
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
      self.client.mutateRow('info_public_monitor',row,mutations,None)
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
    if spider.name not in ['csdnActivity']:
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
