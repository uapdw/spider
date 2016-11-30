# -*- coding: utf-8 -*-

import json
import hashlib
import datetime

import happybase

from spider.items import HBaseItem, SqlalchemyItem


class SqlalchemyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SqlalchemyItem):
            item.save()

        return item


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

        mutations = self._genMutations(item, column_family)

        table = self.connection.table(table_name)
        table.put(row_key, mutations)

        return item

    def _genMutations(self, item, column_family):
        mutations = {}
        for field in item.fields:
            value = item.get(field)
            if value:
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, unicode) or isinstance(value, str):
                    value = value.encode('utf-8')
                else:
                    value = str(value)

            column = '%s:%s' % (column_family, field)
            value = value
            mutations[column] = value
        return mutations
