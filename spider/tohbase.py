# -*- coding: utf-8 -*-

from items import CarDanPinItem

import happybase
import hashlib

class ToHBase:

    def __init__(self):
        self.host = '172.20.3.107'
        self.port = '9090'

    def write(self):
        self.connection = happybase.Connection(self.host, self.port)
        datas = [{'product_id': '623', 'brand': u'北京汽车', 'type': u'北京40'},
                {'product_id': '3417', 'brand': u'北京汽车', 'type': u'绅宝X65'},
                {'product_id': '2027', 'brand': u'长城汽车', 'type': u'哈弗H5'},
                {'product_id': '2123', 'brand': u'长城汽车', 'type': u'哈弗H6'},
                {'product_id': '3481', 'brand': u'长城汽车', 'type': u'哈弗H6 Coupe'},
                {'product_id': '3000', 'brand': u'一汽奔腾', 'type': u'奔腾X80'},
                {'product_id': '3204', 'brand': u'长安汽车', 'type': u'长安CS75'}]
        for data in datas:
            item = CarDanPinItem()
            item['product_id'] = data['product_id']
            item['brand'] = data['brand']
            item['type'] = data['type']
    
            table_name = item.table_name
            row_key = item.get_row_key()
            column_family = item.column_family
    
            row = hashlib.new("md5", row_key).hexdigest()
            mutations = self._genMutations(item, column_family)
    
            table = self.connection.table(table_name)
            table.put(row, mutations)
        self.connection.close()

    def _genMutations(self, item, column_family):
        mutations = {}
        for field in item.fields:
            value = item.get(field)
            if value:
                value = value.encode('utf-8')
            column = '%s:%s' % (column_family, field)
            value = value
            mutations[column] = value
        return mutations

tohbase = ToHBase()
tohbase.write()