# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import pymongo
import hashlib


class HBaseOperator():
	def __init__(self):
		self.host = "172.20.6.61"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)

		conn = pymongo.Connection('localhost',27017)
		self.infoDB = conn.info

	def __del__(self):
		self.transport.close()

	def getAllTablesInfo(self):
		#get table info
		listTables = self.client.getTableNames()
		print "="*40
		print "Show all tables information...."

		for tableName in listTables:
			print "TableName:" + tableName
			print " "
			listColumns = self.client.getColumnDescriptors(tableName)
			print listColumns
			print " "

			listTableRegions = self.client.getTableRegions(tableName)
			print listTableRegions
			print "+"*40

	def deleteInfoTables(self):
		print "Delete info tables...."
		self.client.disableTable('info_public_monitor')
		self.client.deleteTable('info_public_monitor')
		self.client.disableTable('info_data')
		self.client.deleteTable('info_data')

	def createInfoTables(self):
		print "Create info tables...."
		desc = []
		desc.append(ColumnDescriptor('baidu_articles:'))
		desc.append(ColumnDescriptor('other_articles:'))
		desc.append(ColumnDescriptor('report:'))
		desc.append(ColumnDescriptor('weibo:'))
		desc.append(ColumnDescriptor('blog:'))
		desc.append(ColumnDescriptor('activity:'))
		self.client.createTable('info_public_monitor',desc)

		desc = []
		desc.append(ColumnDescriptor('macro_data:'))
		desc.append(ColumnDescriptor('macro_index:'))
		desc.append(ColumnDescriptor('rate:'))
		desc.append(ColumnDescriptor('stock_balancesheet:'))
		desc.append(ColumnDescriptor('stock_cashflow:'))
		desc.append(ColumnDescriptor('stock_companyinfo:'))
		desc.append(ColumnDescriptor('stock_incomestatements:'))
		self.client.createTable('info_data',desc)

	def importBaiduArticlesDatas(self):
		print "Start import baidu articles data...."
		tBaiduArticles = self.infoDB.baidu_articles
		listBaiduArticles = tBaiduArticles.find()
		
		for i in listBaiduArticles:
			rowKey = hashlib.new('md5',i['url']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='baidu_articles:siteName',value=(i['siteName']).encode('utf-8')))
			mutations.append(Mutation(column='baidu_articles:publishTime',value=(i['publishTime']).strftime('%Y-%m-%d %H:%M:%S')))
			mutations.append(Mutation(column='baidu_articles:url',value=i['url']))
			mutations.append(Mutation(column='baidu_articles:title',value=(i['title']).encode('utf-8')))
			mutations.append(Mutation(column='baidu_articles:keyWords',value=(i['keyWords']).encode('utf-8')))
			mutations.append(Mutation(column='baidu_articles:content',value=(i['content']).encode('utf-8')))
			mutations.append(Mutation(column='baidu_articles:addTime',value=(i['addTime']).strftime('%Y-%m-%d %H:%M:%S')))
			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importOtherArticlesDatas(self):
		print "Start import other articles data...."
		tWebArticles = self.infoDB.web_articles
		listWebArticles = tWebArticles.find()
		
		for i in listWebArticles:
			rowKey = hashlib.new('md5',i['url']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='other_articles:siteName',value=(i['siteName']).encode('utf-8')))
			if type(i['publishTime']) == "unicode":
				mutations.append(Mutation(column='other_articles:publishTime',value=(i['publishTime']).encode('utf-8')))
			elif type(i['publishTime']) == "datetime.datetime":
				mutations.append(Mutation(column='other_articles:publishTime',value=(i['publishTime']).strftime('%Y-%m-%d %H:%M:%S')))
			else:
				mutations.append(Mutation(column='other_articles:publishTime',value=''))
			mutations.append(Mutation(column='other_articles:url',value=i['url']))
			mutations.append(Mutation(column='other_articles:title',value=(i['title']).encode('utf-8')))
			mutations.append(Mutation(column='other_articles:keyWords',value=(i['keyWords']).encode('utf-8')))
			mutations.append(Mutation(column='other_articles:content',value=(i['content']).encode('utf-8')))
			mutations.append(Mutation(column='other_articles:addTime',value=(i['addTime']).strftime('%Y-%m-%d %H:%M:%S')))
			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importBlogDatas(self):
		print "Start import blog data...."
		tWebBlogs = self.infoDB.web_blogs
		listWebBlogs = tWebBlogs.find()
		
		for i in listWebBlogs:
			rowKey = hashlib.new('md5',i['url']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='blog:siteName',value=(i['siteName']).encode('utf-8')))
			mutations.append(Mutation(column='blog:url',value=i['url']))
			mutations.append(Mutation(column='blog:title',value=(i['title']).encode('utf-8')))
			mutations.append(Mutation(column='blog:content',value=(i['content']).encode('utf-8')))
			mutations.append(Mutation(column='blog:addTime',value=(i['addTime']).strftime('%Y-%m-%d %H:%M:%S')))
			mutations.append(Mutation(column='blog:author',value=(i['author']).encode('utf-8')))
			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importActivityDatas(self):
		print "Start import activity data...."
		tActivity = self.infoDB.web_activity
		listActivity = tActivity.find()
		
		for i in listActivity:
			rowKey = hashlib.new('md5','activity_'+i['activityID']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='activity:activityID',value=i['activityID']))
			mutations.append(Mutation(column='activity:addTime',value=(i['addTime']).strftime('%Y-%m-%d %H:%M:%S')))
			mutations.append(Mutation(column='activity:keyWords',value=(i['keyWords']).encode('utf-8')))
			mutations.append(Mutation(column='activity:location',value=(i['location']).encode('utf-8')))
			mutations.append(Mutation(column='activity:siteName',value=i['siteName']))
			mutations.append(Mutation(column='activity:time',value=(i['time']).encode('utf-8')))
			mutations.append(Mutation(column='activity:title',value=(i['title']).encode('utf-8')))
			mutations.append(Mutation(column='activity:trad',value=(i['trad']).encode('utf-8')))
			mutations.append(Mutation(column='activity:url',value=i['url']))
			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importReportDatas(self):
		print "Start import report data...."
		tInfReport = self.infoDB.IndustryReport
		listInfReport = tInfReport.find()
		
		for i in listInfReport:
			rowKey = hashlib.new('md5',i['url']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='report:siteName',value=(i['siteName']).encode('utf-8')))
			mutations.append(Mutation(column='report:url',value=i['url']))
			mutations.append(Mutation(column='report:title',value=(i['title']).encode('utf-8')))
			mutations.append(Mutation(column='report:source',value=(i['source']).encode('utf-8')))
			mutations.append(Mutation(column='report:addTime',value=(i['addTime']).strftime('%Y-%m-%d %H:%M:%S')))
			if type(i['publishTime']) == "unicode":
				mutations.append(Mutation(column='report:publishTime',value=(i['publishTime']).encode('utf-8')))
			elif type(i['publishTime']) == "datetime.datetime": 
				mutations.append(Mutation(column='report:publishTime',value=(i['publishTime']).strftime('%Y-%m-%d %H:%M:%S')))
			else:
				mutations.append(Mutation(column='report:publishTime',value=i['publishTime']))

			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importWeiboDatas(self):
		print "Start import weibo data...."
		tWeiboContent = self.infoDB.wb_content
		listWeiboContent = tWeiboContent.find()
		
		for i in listWeiboContent:
			rowKey = hashlib.new('md5',i['mid']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='weibo:user_id',value=str(i['user_id'])))
			mutations.append(Mutation(column='weibo:content',value=(i['text']).encode('utf-8')))
			mutations.append(Mutation(column='weibo:screen_name',value=(i['screen_name']).encode('utf-8')))
			mutations.append(Mutation(column='weibo:comments_count',value=str(i['comments_count'])))
			mutations.append(Mutation(column='weibo:reposts_count',value=str(i['reposts_count'])))
			mutations.append(Mutation(column='weibo:created_at',value=(i['created_at']).strftime('%Y-%m-%d %H:%M:%S')))
			self.client.mutateRow('info_public_monitor',rowKey,mutations,None)

	def importMacroData(self):
		print "Start import macro data...."
		tMacroData = self.infoDB.bm_macro_data
		listMacroData = tMacroData.find()
		
		for i in listMacroData:
			rowKey = hashlib.new('md5',i['key']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='macro_data:area',value=i['area']))
			mutations.append(Mutation(column='macro_data:code',value=i['code']))
			mutations.append(Mutation(column='macro_data:desc',value=(i['desc']).encode('utf-8')))
			mutations.append(Mutation(column='macro_data:mdate',value=str(i['mdate'])))
			mutations.append(Mutation(column='macro_data:name',value=(i['name']).encode('utf-8')))
			mutations.append(Mutation(column='macro_data:qdate',value=str(i['qdate'])))
			mutations.append(Mutation(column='macro_data:ts',value=str(i['ts'])))
			mutations.append(Mutation(column='macro_data:value',value=str(i['value'])))
			mutations.append(Mutation(column='macro_data:ydate',value=str(i['ydate'])))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importMacroIndexData(self):
		print "Start import macro index data...."
		tMacroIndex = self.infoDB.bm_macro_index
		listMacroIndex = tMacroIndex.find()
		
		for i in listMacroIndex:
			rowKey = hashlib.new('md5',i['code']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='macro_index:code',value=i['code']))
			mutations.append(Mutation(column='macro_index:name',value=(i['name']).encode('utf-8')))
			mutations.append(Mutation(column='macro_index:ts',value=str(i['ts'])))
			mutations.append(Mutation(column='macro_index:parentcode',value=i['parentcode']))
			mutations.append(Mutation(column='macro_index:period',value=i['period']))
			mutations.append(Mutation(column='macro_index:note',value=(i['note']).encode('utf-8')))
			mutations.append(Mutation(column='macro_index:ifdata',value=i['ifdata']))
			if type(i['unit']) == 'unicode':
				mutations.append(Mutation(column='macro_index:unit',value=(i['unit']).encode('utf-8')))
			else:
				mutations.append(Mutation(column='macro_index:unit',value=''))

			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importRateDatas(self):
		print "Start import rate data...."
		tRate = self.infoDB.bm_rate
		listRate = tRate.find()
		
		for i in listRate:
			rowKey = hashlib.new('md5',i['key']).hexdigest()
			mutations = []
			mutations.append(Mutation(column='rate:bocprice',value=i['bocprice']))
			mutations.append(Mutation(column='rate:currentname',value=(i['currentname']).encode('utf-8')))
			mutations.append(Mutation(column='rate:midprice',value=i['midprice']))
			mutations.append(Mutation(column='rate:note',value=(i['note']).encode('utf-8')))
			mutations.append(Mutation(column='rate:price_cash_in',value=i['price_cash_in']))
			mutations.append(Mutation(column='rate:price_cash_out',value=i['price_cash_out']))
			mutations.append(Mutation(column='rate:price_spot_in',value=i['price_spot_in']))
			mutations.append(Mutation(column='rate:price_spot_out',value=i['price_spot_out']))
			mutations.append(Mutation(column='rate:releasetime',value=(i['releasetime']).strftime('%Y-%m-%d %H:%M:%S')))
			mutations.append(Mutation(column='rate:ts',value=str(i['ts'])))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importStockBalanceSheet(self):
		print "Start import stock balance sheet ...."
		tStockBalanceSheet = self.infoDB.stock_balancesheet
		listStockBalanceSheet = tStockBalanceSheet.find()
		
		for i in listStockBalanceSheet:
			mutations = []
			rowKey = hashlib.new('md5','balancesheet_'+i['stockCode']+'_'+i['pubtime']).hexdigest()
			for key in i:
				if key == '_id':
					continue
				mutations.append(Mutation(column='stock_balancesheet:' + key.encode('utf-8'),value=(i[key]).encode('utf-8')))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importStockCashFlow(self):
		print "Start import stock cash flow ...."
		tStockCashFlow = self.infoDB.stock_cashflow
		listStockCashFlow = tStockCashFlow.find()
		
		for i in listStockCashFlow:
			mutations = []
			rowKey = hashlib.new('md5','cashflow_'+i['stockCode']+'_'+i['pubtime']).hexdigest()
			for key in i:
				if key == '_id':
					continue
				mutations.append(Mutation(column='stock_cashflow:' + key.encode('utf-8'),value=(i[key]).encode('utf-8')))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importStockIncomeStatements(self):
		print "Start import stock income statements...."
		tStockIncomeStatements = self.infoDB.stock_incomestatements
		listStockIncomeStatements = tStockIncomeStatements.find()
		
		for i in listStockIncomeStatements:
			mutations = []
			rowKey = hashlib.new('md5','income_'+i['stockCode']+'_'+i['pubtime']).hexdigest()
			for key in i:
				if key == '_id':
					continue
				mutations.append(Mutation(column='stock_incomestatements:' + key.encode('utf-8'),value=(i[key]).encode('utf-8')))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importStockCompanyInfo(self):
		print "Start import stock company info...."
		tStockCompanyInfo = self.infoDB.stock_companyinfo
		listStockCompanyInfo = tStockCompanyInfo.find()
		
		for i in listStockCompanyInfo:
			mutations = []
			rowKey = hashlib.new('md5','companyinfo_'+i['stockCode']).hexdigest()
			for key in i:
				if key == '_id':
					continue
				mutations.append(Mutation(column='stock_companyinfo:' + key.encode('utf-8'),value=(i[key]).encode('utf-8')))
			self.client.mutateRow('info_data',rowKey,mutations,None)

	def importAllDatas(self):
		#self.deleteInfoTables()
		self.createInfoTables()

		self.importBaiduArticlesDatas()
		self.importOtherArticlesDatas()
		self.importBlogDatas()
		self.importReportDatas()
		self.importWeiboDatas()
		self.importActivityDatas()
		self.importMacroData()
		self.importMacroIndexData()
		self.importRateDatas()
		self.importStockBalanceSheet()
		self.importStockCashFlow()
		self.importStockIncomeStatements()
		self.importStockCompanyInfo()

			
		
def main():
	ho = HBaseOperator()
	ho.importAllDatas()


if __name__ == "__main__":
	main()
