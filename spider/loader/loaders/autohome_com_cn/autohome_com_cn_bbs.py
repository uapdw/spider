# -*- coding: utf-8 -*-

import re

from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from spider.loader.loaders import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor)
from spider.items import UradarBBSItem


class AutohomeComCnBBSLoader(object):

    u"""汽车之家BBS"""

    id_matcher = re.compile(
        '.*club\.autohome\.com\.cn/bbs/thread(qa)?-(\S+-\d+)-(\d+)-\d+\.html'
    )

    def load(self, response):
        ti = self.load_thread(response)

        i_list = []
        for selector in Selector(response).xpath(
                '//*[@id="maxwrap-maintopic"]/div[2]'):
            i = self.load_post(selector, ti['url'])
            i_list.append(i)

        for selector in Selector(response).xpath(
                '//*[@id="maxwrap-reply"]/div'):
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
            l.add_value('thread_id', match.group(2))
        else:
            raise DropItem('not thread_id')

        l.add_value('url', response.url)
        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))
        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))
        l.add_value('source', None)
        l.add_value('site_domain', 'autohome.com.cn')
        l.add_value('site_name', u'汽车之家')
        l.add_value('sentiment', None)

        return l.load_item()

    def load_post(self, selector, base_url):
        l = ItemLoader(item={}, selector=selector)
        l.default_output_processor = TakeFirst()

        l.add_xpath('title', '//*[contains(@class, "rtitle")]',
                    MapCompose(text))
        l.add_xpath('content', '//*[@xname="content"]',
                    MapCompose(SafeHtml(base_url)))
        l.add_xpath('author', '//*[@xname="uname"]', MapCompose(text))
        l.add_xpath('publish_time', '@data-time',
                    MapCompose(DateProcessor('%Y%m%d%H%M%S')))
        l.add_xpath('post_id', '@id', MapCompose(text),
                    MapCompose(RegexProcessor('F(\d+)')))

        return l.load_item()
