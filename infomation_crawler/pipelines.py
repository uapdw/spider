# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime
from scrapy.exceptions import DropItem

class BaiduNewsPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['baidu']:
	return item

      article = {"title":item['title'][0],'sitename':item['sitename'][0],'posttime':item['posttime'][0]}
      spider.tArticles.update({'link':item['href'][0]},{'$set':article},True)
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
    if spider.name not in ['csdn', 'it168']:
      return item

    print "enter WebArticlePipeLine...."
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no article item: %s" % item)
    else:
      data = {'title':item['title'],'addTime':item['addTime'],'content':item['content'],'siteName':item['siteName']}
      spider.tWebArticles.update({'url':item['url']},{'$set':data},True)
      return item

class WebBlogPipeLine(object):
  def process_item(self, item, spider):
    if spider.name not in ['iteye']:
      return item

    print "enter WebBlogPipeLine...."
    if item['title'] == '' or item['content'] == '':
      raise DropItem("there is no blog item: %s" % item)
    else:
      data = {'title':item['title'],'addTime':item['addTime'],'content':item['content'],'siteName':item['siteName'],'author':item['author']}
      spider.tWebBlogs.update({'url':item['url']},{'$set':data},True)
      return item

