# -*- coding: utf-8 -*-

import json
import hashlib
import datetime

import pysolr
import happybase
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline

from spider.items import HBaseItem, SqlalchemyItem, StockReportItem
from spider.loader.processors import text


class SqlalchemyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SqlalchemyItem):
            item.add()

        return item


class NamedFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, StockReportItem):
            for file_spec in item['file_urls']:
                yield Request(
                    url=file_spec["file_url"],
                    meta={"file_spec": file_spec, "download_timeout": 180}
                )

    def file_path(self, request, response=None, info=None):
        return request.meta["file_spec"]["file_name"]


class StdOutPipeline(object):
    '''stdout pipeline'''

    def process_item(self, item, spider):
        for field in item:
            print '%s:%s' % (field, item[field])
        return item


class JSONWriterPipeline(object):

    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filename='items.jl'
        )

    def open_spider(self, spider):
        self.file = open(self.filename, 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        if isinstance(item, HBaseItem):
            item.validate()

        line = self._genItemLine(item) + "\n"
        self.file.write(line)
        return item

    def _genItemLine(self, item):
        item_dict = {}
        for field in item:
            v = item[field]
            if (isinstance(v, datetime.datetime)
                    or isinstance(v, datetime.date)):
                v = v.strftime("%Y-%m-%d %H:%M:%S")
            item_dict[field] = v
        return json.dumps(item_dict)


class SolrItemPipeline(object):
    '''Solr Pipeline'''

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SOLR_HOST'),
            port=crawler.settings.get('SOLR_PORT')
        )

    def open_spider(self, spider):
        self.solr_dict = {}

    def close_spider(self, spider):
        pass

    def get_solr(self, index_name):
        if index_name in self.solr_dict:
            return self.solr_dict[index_name]
        else:
            self.solr_dict[index_name] = pysolr.Solr(
                'http://%s:%s/solr/%s' % (
                    self.host,
                    self.port,
                    index_name
                )
            )
            return self.solr_dict[index_name]

    def process_item(self, item, spider):

        if not isinstance(item, HBaseItem):
            return

        item.validate()

        solr = self.get_solr(item.table_name)

        doc = self._gen_doc(item)

        # 更新、新增doc
        solr.add([doc])

        return item

    def _gen_doc(self, item):
        doc = {}

        # id和hbase中row key相同
        row_key = item.get_row_key()
        doc['id'] = hashlib.new("md5", row_key).hexdigest()

        for field in item.fields:
            value = item.get(field)
            if value:
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    pass
                    # value = value.encode('utf-8')

            doc[field] = value

        # title_nt值和title相同
        doc['title_nt'] = doc['title']

        # content去掉标签
        doc['content_with_html_tags'] = doc['content']
        doc['content'] = text(doc['content'])

        return doc


class HBaseItemPipeline(object):
    '''HBase Pipeline'''

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HBASE_HOST'),
            port=crawler.settings.get('HBASE_PORT')
        )

    def open_spider(self, spider):
        self.connection = happybase.Connection(self.host, self.port)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if not isinstance(item, HBaseItem):
            return

        item.validate()

        table_name = item.table_name
        row_key = item.get_row_key()
        column_family = item.column_family

        row = hashlib.new("md5", row_key).hexdigest()
        mutations = self._genMutations(item, column_family)

        table = self.connection.table(table_name)
        table.put(row, mutations)

        return item

    def _genMutations(self, item, column_family):
        mutations = {}
        for field in item.fields:
            value = item.get(field)
            if value:
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    value = value.encode('utf-8')

            column = '%s:%s' % (column_family, field)
            value = value
            mutations[column] = value
        return mutations


# class StockCompanyInfoPipeline(object):
#     def process_item(self, item, spider):
#         if spider.name not in ['stockinfo']:
#             return item
#         print "enter StockCompanyInfoPipeline....."
#
#         arrInfo = {}
#         for i in item:
#             if i == 'stockCode':
#                 continue
#             arrInfo[i] = item[i]
#
#         spider.tCompanyInfo.update({'stockCode': item['stockCode']}, {'$set': arrInfo}, True)
#         return item
#
#
# class StockBalanceSheetPipeline(object):
#     def process_item(self, item, spider):
#         if spider.name not in ['stockbalance']:
#             return item
#         print "enter StockBalanceSheetPipeline....."
#
#         arrInfo = {}
#         if u'科目'.encode('utf8') in item['row']:
#             for i in item['row']:
#                 if i == 'stockCode' or i == 'pubtime':
#                     continue
#                 arrInfo[i] = item['row'][i]
#
#             spider.tBalanceSheet.update({'stockCode': item['row']['stockCode'], 'pubtime': item['row']['pubtime']}, {'$set': arrInfo}, True)
#             return item
#         else:
#             raise DropItem('No stock balance sheet datas in %s' % item)
#
#
# class StockIncomeStatementsPipeline(object):
#     def process_item(self, item, spider):
#         if spider.name not in ['stockincome']:
#             return item
#         print "enter StockIncomeStatementsPipeline....."
#
#         arrInfo = {}
#         if u'科目'.encode('utf8') in item['row']:
#             for i in item['row']:
#                 if i == 'stockCode' or i == 'pubtime':
#                     continue
#                 arrInfo[i] = item['row'][i]
#
#             spider.tIncome.update({'stockCode': item['row']['stockCode'], 'pubtime': item['row']['pubtime']}, {'$set': arrInfo}, True)
#             return item
#         else:
#             raise DropItem('No stock income statements datas in %s' % item)
#
#
# class StockCashFlowPipeline(object):
#     def process_item(self, item, spider):
#         if spider.name not in ['stockcashflow']:
#             return item
#         print "enter StockCashFlowPipeline....."
#
#         arrInfo = {}
#         if u'科目'.encode('utf8') in item['row']:
#             for i in item['row']:
#                 if i == 'stockCode' or i == 'pubtime':
#                     continue
#                 arrInfo[i] = item['row'][i]
#
#             spider.tCashFlow.update({'stockCode': item['row']['stockCode'], 'pubtime': item['row']['pubtime']}, {'$set': arrInfo}, True)
#             return item
#         else:
#             raise DropItem('No stock cash flow datas in %s' % item)
#
#
# class StockFinancialReportPipeline(object):
#     def process_item(self, item, spider):
#         if spider.name not in ['cninfo']:
#             return item
#         else:
#             if item['iType'] == 'financialReport':
#                 print "enter StockFinancialReportPipeline....."
#                 print '='*10
#             return item
