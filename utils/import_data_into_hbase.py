from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import pymongo


class HBaseOperator():
	def __init__(self):
		self.host = "172.20.6.62"
		self.port = 9090
		self.transport = TBufferedTransport(TSocket(self.host, self.port))
		self.transport.open()
		self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Hbase.Client(self.protocol)

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
		self.client.deleteTable('info_public_monitor')
		self.client.deleteTable('info_data')

	def createInfoTables(self):
		#create tables
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

	def importArticleDatas(self):
		#insert data
		row = 'row-key1'
		mutations = [Mutation(column='c1:1',value="123123")]
		self.client.mutateRow('Mytable',row,mutations,None)
		
def main():
	ho = HBaseOperator()
	#ho.getAllTablesInfo()
	#ho.createInfoTables()
	ho.deleteInfoTables()


if __name__ == "__main__":
	main()






