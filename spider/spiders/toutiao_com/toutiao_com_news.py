# -*- coding: utf-8 -*-

__author__ = 'liufeng'

import re
import json
import time

from scrapy import Spider
from scrapy.http import Request
from scrapy.loader.processors import TakeFirst, MapCompose

from spider.loader import ItemLoader
from spider.items import UradarNewsItem
from spider.loader.processors import (text, safe_html,
                                      DateProcessor, PipelineProcessor)


class ArticleToutiaoSpider(Spider):

    name = "toutiao_com_news"
    allowed_domains = ["toutiao.com"]
    start_urls = [
        'http://toutiao.com/'
    ]

    url_pattern = 'http://toutiao.com/api/article/recent/?source=2&count=20&category=__all__&max_behot_time=%s&utm_source=toutiao&offset=0'

    toutiao_article_url_pattern = '.*toutiao\.com/.*'
    article_matcher = re.compile(toutiao_article_url_pattern)

    def _get_data_url(self, max_behot_time):
        return self.url_pattern % max_behot_time

    def parse(self, response):
        return self.parse_start(response)

    def parse_start(self, response):
        match = re.match(
            r'.*\'max_behot_time\':\s*\'([\d|\.]+)\'',
            response.body,
            re.DOTALL
        )

        if match:
            max_behot_time = match.group(1)
            yield Request(
                self._get_data_url(max_behot_time),
                callback=self.parse_next,
                meta={'jump': 0}
            )

    def parse_next(self, response):
        json_data = json.loads(response.body)
        for data in json_data['data']:
            if self.article_matcher.match(data['article_url']):
                yield Request(
                    data['article_url'],
                    callback=self.parse_news,
                    meta={'abstract': data['abstract']}
                )

        if response.meta['jump'] < 50:
            yield Request(
                self._get_data_url(json_data['next']['max_behot_time']),
                callback=self.parse_next,
                meta={'jump': response.meta['jump'] + 1}
            )

    def parse_news(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="title"]/h1', MapCompose(text))

        l.add_xpath('content', '//*[@class="article-content"]',
                    MapCompose(safe_html))

        l.add_xpath('publish_time', '//*[@class="time"]', MapCompose(
            PipelineProcessor(
                text,
                DateProcessor('%Y-%m-%d %H:%M')
            )
        ))

        l.add_xpath('source', '//*[@class="profile_avatar"]',
                    MapCompose(text))

        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))

        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))

        l.add_value('site_domain', 'toutiao.com')
        l.add_value('site_name', u'今日头条')

        i = l.load_item()
        return i
