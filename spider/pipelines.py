# -*- coding: utf-8 -*-

import json
import hashlib
import datetime

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import Mutation
import pysolr

from spider.items import HBaseItem
from spider.loader.processors import text


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

    def __init__(self, host, port, index):
        self.host = host
        self.port = port
        self.index = index

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SOLR_HOST'),
            port=crawler.settings.get('SOLR_PORT'),
            index=crawler.settings.get('SOLR_INDEX')
        )

    def open_spider(self, spider):
        self.solr = pysolr.Solr(
            'http://%s:%s/solr/%s' % (
                self.host,
                self.port,
                self.index
            )
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        if not isinstance(item, HBaseItem):
            return

        item.validate()

        doc = self._gen_doc(item)

        # 更新、新增doc
        self.solr.add([doc])

        return item

    def _gen_doc(self, item):
        doc = {}

        # id和hbase中row key相同
        row_key_field = item.row_key_field
        doc['id'] = hashlib.new("md5", item[row_key_field]).hexdigest()

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

        return item

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
