# -*- coding: utf-8 -*-

from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.selector import Selector
from spider.loader import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor, PipelineProcessor)
from spider.items import CarComDetailItem
from urllib import quote

class AutohomeBQLoader:
    u"""汽车之家新闻爬虫"""

    comment_id_xpath = '//div[@class="fn-right js-collectionbox"]/a/@data-val'
#     product_id_xpath = '//div[@class="breadnav"]'
#     content_xpath = '//div[@class="mouth-main"]/div[@class="mouth-item"][last()]/div[@class="text-con"]'
    author_xpath = '//div[@class="user-name"]/a'
#     publish_time_xpath = '//div[@class="mouth-main"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_format = '%Y%m%d'

    def load(self, response):
        ti = self.load_base(response)

        i_list = []
        for index, selector in enumerate(Selector(response).xpath(
                '//div[@class="mouth-main"]/div')):
            
            i = self.load_ext(selector, index, ti['url'])
            i_list.append(i)

        item_list = []
        for i in i_list:
            item = ti.copy()
            for key, value in i.iteritems():
                item[key] = value
            item_list.append(item)

        return item_list

    def load_base(self, response):
        l = ItemLoader(item=CarComDetailItem(), response=response)

        l.default_output_processor = TakeFirst()

#         l.add_xpath('comment_id', self.comment_id_xpath, MapCompose(text))

        l.add_value('product_id', response.url.split(quote('|'.encode('gbk')))[1])

        l.add_value('url', response.url)

#         l.add_xpath('content', self.content_xpath,
#                     MapCompose(SafeHtml(response.url)), Join('\n'))

        # author可选
        l.add_xpath('author', self.author_xpath, MapCompose(text))

        i = l.load_item()
        return i

    def load_ext(self, selector, index, base_url):
        
        if selector.xpath('div[@class="text-con"]/*[@class="add-dl"]').extract():
            content_xpath = 'div[@class="text-con"]/*[@class="add-dl"]/dd[@class="add-dl-text"]'
        else:
            content_xpath = 'div[@class="text-con"]'
        
        l = ItemLoader(item={}, selector=selector)
        l.default_output_processor = TakeFirst()

        l.add_xpath('comment_id', self.comment_id_xpath, MapCompose(text))

        l.add_xpath('content', content_xpath,
                    MapCompose(SafeHtml(base_url)))

        # publish_time_re可选
        processor_list = [text]

        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is not None:
            processor_list.append(
                RegexProcessor(
                    publish_time_re,
                    join_str=getattr(self, 'publish_time_re_join', u'')
                )
            )

        processor_list.append(DateProcessor(self.publish_time_format))

        l.add_xpath('publish_time', 'div[@class="cont-title fn-clear"]',
                    MapCompose(
                        PipelineProcessor(
                            *processor_list
                        )
                    ))
        
        i = l.load_item()
        i['comment_id'] = '%s_%s' % (i['comment_id'], index)

        return i
