# -*- coding: utf-8 -*-

import re

from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from spider.loader.loaders import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor)
from spider.items import UradarBBSItem


class SinaComCnBBSLoader(object):

    u"""新浪汽车BBS"""

    id_matcher = re.compile(
        '.*bbs\.auto\.sina\.com\.cn/.*thread-(\d+)-\d+-\d+\.html'
    )

    def load(self, response):
        ti = self.load_thread(response)

        i_list = []
        for selector in Selector(response).xpath(
                '//*[@name="modactions"]/div[contains(@class, "viewthread")]'):
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
        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))
        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))
        l.add_value('source', None)
        l.add_value('site_domain', 'sina.com.cn')
        l.add_value('site_name', u'新浪')
        l.add_value('sentiment', None)

        return l.load_item()

    def load_post(self, selector, base_url):
        l = ItemLoader(item={}, selector=selector)
        l.default_output_processor = TakeFirst()
        l.add_xpath('title', '//*[@name="modactions"]//h1', MapCompose(text))
        l.add_xpath('content', '//*[contains(@class, "postmessage")]',
                    MapCompose(SafeHtml(base_url)))
        l.add_xpath('author', '//*[@class="postauthor"]/cite/a/text()',
                    MapCompose(text))
        l.add_xpath('publish_time', '//*[@class="postinfo"]/text()[2]',
                    MapCompose(RegexProcessor(
                        u'\s*发表于\s*(\d{4}-\d{1,2}-\d{1,2})\s*(\d{1,2}:\d{1,2})', ' '
                    )),
                    MapCompose(DateProcessor('%Y-%m-%d %H:%M')))
        l.add_xpath('post_id', 'table/@id',
                    MapCompose(text))

        return l.load_item()
