# -*- coding: utf-8 -*-

import datetime
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.items import UradarActivityItem
from spider.loader.processors import (text, PipelineProcessor,
                                      RegexProcessor, SafeHtml)


class CSDNActivitySpider(CrawlSpider):

    u"""CSDN活动爬虫"""

    name = 'csdn_net_activity'
    allowed_domains = ['csdn.net']
    start_urls = ['http://huiyi.csdn.net/']

    rules = (
        Rule(LinkExtractor(
            allow=(
                'huiyi\.csdn\.net/activity/product/goods_list\?project_id=\d+'
            )
        ), callback='parse_activity'),
        Rule(LinkExtractor(
            allow=('huiyi\.csdn\.net/activity/home\?&page=\d+')
        ))
    )

    def parse_activity(self, response):
        l = ItemLoader(item=UradarActivityItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="con"]/dt/h2',
                    MapCompose(text))

        l.add_xpath('content', '//*[@class="guests-intro"]',
                    MapCompose(SafeHtml(response.url)), Join('\n'))

        l.add_xpath('location', '//*[@class="con"]/dd',
                    MapCompose(PipelineProcessor(
                               text,
                               RegexProcessor('\s*(\S+).*'))))

        l.add_xpath('trad', '//*[@class="submit"]/span',
                    MapCompose(PipelineProcessor(
                               text,
                               RegexProcessor(u'.*总费用:\s*(\S+).*'))))

        time_dict = self._parse_start_end_time(response)
        if time_dict:
            l.add_value('start_time', time_dict['start_time'])
            l.add_value('end_time', time_dict['end_time'])

        i = l.load_item()
        return i

    def _parse_start_end_time(self, response):
        l = ItemLoader(item={}, response=response)
        l.default_output_processor = TakeFirst()

        l.add_xpath(
            'right_time_range',
            '//*[@class="addr-time"]/ul/li[1]',
            MapCompose(text)
        )

        l.add_xpath(
            'top_time_range',
            '//*[@class="con"]/dd',
            MapCompose(text)
        )

        time_item = l.load_item()
        right_time_range = time_item.get('right_time_range')
        top_time_range = time_item.get('top_time_range')

        if not right_time_range or not top_time_range:
            return

        time_dict = {}

        match = re.match(u'''.*时间：(\d{2})月(\d{2})日\s*(\d{2})时(\d{2})分\s*--\s*(\d{2})月(\d{2})日\s*(\d{2})时(\d{2})分.*''', right_time_range)
        if match:
            time_dict['start_time'] = {
                'month': match.group(1),
                'day': match.group(2),
                'hour': match.group(3),
                'minute': match.group(4)
            }
            time_dict['end_time'] = {
                'month': match.group(5),
                'day': match.group(6),
                'hour': match.group(7),
                'minute': match.group(8)
            }

        if not time_dict:
            match = re.match(u'''.*时间：(\d{2})月(\d{2})日\s*(\d{2})时(\d{2})分\s*--\s*(\d{2})时(\d{2})分.*''', right_time_range)
            if match:
                time_dict['start_time'] = {
                    'month': match.group(1),
                    'day': match.group(2),
                    'hour': match.group(3),
                    'minute': match.group(4)
                }
                time_dict['end_time'] = {
                    'month': match.group(1),
                    'day': match.group(2),
                    'hour': match.group(5),
                    'minute': match.group(6)
                }

        if not time_dict:
            return

        years = re.findall(u'(\d+)年', top_time_range)

        if not years:
            return

        if len(years) == 2:
            time_dict['start_time']['year'] = years[0]
            time_dict['end_time']['year'] = years[1]
        else:
            time_dict['start_time']['year'] = years[0]
            time_dict['end_time']['year'] = years[0]

        start_time = datetime.datetime(int(time_dict['start_time']['year']),
                                       int(time_dict['start_time']['month']),
                                       int(time_dict['start_time']['day']),
                                       int(time_dict['start_time']['hour']),
                                       int(time_dict['start_time']['minute']))

        end_time = datetime.datetime(int(time_dict['end_time']['year']),
                                     int(time_dict['end_time']['month']),
                                     int(time_dict['end_time']['day']),
                                     int(time_dict['end_time']['hour']),
                                     int(time_dict['end_time']['minute']))

        return {
            'start_time': start_time,
            'end_time': end_time
        }
