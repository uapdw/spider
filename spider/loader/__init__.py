# -*- coding: utf-8 -*-

'''补充https://github.com/scrapy/scrapy的loader目录'''

from scrapy.loader import ItemLoader as ScrapyItemLoader


class ItemLoader(ScrapyItemLoader):
    '''继承scrapy的ItemLoader，增加若干功能'''

    def __init__(self, *args, **kargs):
        ScrapyItemLoader.__init__(self, *args, **kargs)

    def get_value(self, value, *processors, **kw):
        value = super(ItemLoader, self).get_value(value, *processors, **kw)

        regex_end = kw.get('re_end', None)
        if regex_end:
            value = super(ItemLoader, self).get_value(value, re=regex_end)

        return value
