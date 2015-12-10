# -*- coding: utf-8 -*-

import hashlib
import datetime

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import Mutation

from spider.items import HBaseItem


class StdOutPipeline(object):
    '''stdout pipeline'''

    def process_item(self, item, spider):
        for field in item:
            print '%s:%s' % (field, item[field])


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
        item.validate()
        line = self._genItemLine(item) + "\n\n"
        self.file.write(line)

    def _genItemLine(self, item):
        l = []
        for field in item:
            v = item[field]
            if v is None:
                v = ''
            elif isinstance(v, str):
                pass
            elif isinstance(v, int):
                v = str(v)
            elif isinstance(v, unicode):
                v = v.encode('utf-8')
            elif (isinstance(v, datetime.datetime)
                    or isinstance(v, datetime.date)):
                v = v.strftime("%Y-%m-%d %H:%M:%S")

            l.append('%s:%s' % (field, v))
        return '\n'.join(l)


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
        self.transport = TBufferedTransport(TSocket(self.host, self.port))
        self.transport.open()
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(protocol)

    def close_spider(self, spider):
        self.transport.close()

    def process_item(self, item, spider):
        if not isinstance(item, HBaseItem):
            return

        item.validate()

        table_name = item.table_name
        row_key_field = item.row_key_field
        column_family = item.column_family

        row = hashlib.new("md5", item[row_key_field]).hexdigest()
        mutations = self._genMutations(item, column_family)
        self.client.mutateRow(table_name, row, mutations, None)

    def _genMutations(self, item, column_family):
        mutations = []
        for field in item.fields:
            value = item.get(field)
            if value:
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    value = value.encode('utf-8')

            mutation = Mutation(
                column='%s:%s' % (column_family, field),
                value=value
            )
            mutations.append(mutation)
        return mutations
