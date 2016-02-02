# -*- coding: utf-8 -*-

import re

from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from spider.loader.loaders import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor)
from spider.items import UradarBBSItem


class XcarComCnBBSLoader(object):

    u"""爱卡汽车BBS"""

    id_matcher = re.compile(
        '.*viewthread\.php\?.*tid=(\d+).*'
    )

    def load(self, response):
        ti = self.load_thread(response)

        i_list = []
        for selector in Selector(response).xpath(
            '//*[@id="mainNew"]//form[@name="delpost"]/div[@class="F_box_2"]'
        ):
            i = self.load_post(selector, ti['url'])
            i_list.append(i)

        item_list = []
        for i in i_list:
            item = ti.copy()
            for key, value in i.iteritems():
                item[key] = value
            item_list.append(item)

        return item_list

    def load_thread(self, response):
        l = ItemLoader(item=UradarBBSItem(), response=response)

        l.default_output_processor = TakeFirst()

        match = self.id_matcher.match(response.url)
        if match:
            l.add_value('thread_id', match.group(1))
        else:
            raise DropItem('not thread_id')

        l.add_value('url', response.url)
        l.add_xpath('title', '//h1[@class="title"]', MapCompose(text))
        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))
        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))
        l.add_value('source', None)
        l.add_value('site_domain', 'xcar.com.cn')
        l.add_value('site_name', u'爱卡汽车')
        l.add_value('sentiment', None)

        return l.load_item()

    def load_post(self, selector, base_url):
        l = ItemLoader(item={}, selector=selector)
        l.default_output_processor = TakeFirst()
        l.add_xpath('content', 'table/tr[1]/td[2]/table/tr[2]',
                    MapCompose(SafeHtml(base_url)))
        l.add_xpath('author', 'table/tr[1]/td[1]/a[2]/text()',
                    MapCompose(text))
        l.add_xpath(
            'publish_time',
            'table/tr[1]/td[2]/table/tr[1]/td[1]/div[1]/div[2]/text()',
            MapCompose(RegexProcessor(
                u'\s*发表于\s*(\d{4}-\d{2}-\d{2})\s*(\d{2}:\d{2})', ' ')),
            MapCompose(DateProcessor('%Y-%m-%d %H:%M'))
        )
        l.add_xpath(
            'post_id',
            'table/tr[1]/td[2]/table/tr[1]/td[1]/div[1]/div[1]/a/text()',
            MapCompose(text),
            MapCompose(RegexProcessor(u'(\d+)楼'))
        )

        return l.load_item()
