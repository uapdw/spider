# -*- coding: utf-8 -*-

import re
import json

from scrapy.http import Request
from scrapy import FormRequest
from scrapy import Spider
from scrapy.loader.processors import TakeFirst, MapCompose, Join


from spider.loader import ItemLoader
from spider.items import UradarNewsItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      safe_html)


class HuxiuNewsSpider(Spider):
    '''虎嗅网新闻'''

    name = 'huxiu_com_news'
    allowed_domains = ['huxiu.com']
    start_urls = [
        'http://www.huxiu.com/'
    ]

    article_list_url = 'http://www.huxiu.com/v2_action/article_list'

    def parse(self, response):
        return self.parse_start(response)

    def _generate_news_page_requests(self, aid_list):
        request_list = []

        if aid_list:
            for aid in aid_list:
                request_list.append(
                    Request(
                        'http://www.huxiu.com/article/%s/1.html' % aid,
                        callback=self.parse_news
                    )
                )

        return request_list

    def parse_start(self, response):
        request_list = []

        l = ItemLoader(item={}, response=response)
        l.add_xpath('url', '//*[@class="mod-info-flow"]/\
                            div[contains(@class, "mod-b mod-art")]/@data-aid')
        id_item = l.load_item()

        if 'url' in id_item:
            request_list.extend(
                self._generate_news_page_requests(id_item['url'])
            )

        match = re.match(
            '.*huxiu_hash_code\s*=\s*["|\'](\S+)["|\']',
            response.body,
            re.DOTALL
        )

        if match:
            huxiu_hash_code = match.group(1)
            request_list.append(
                self._generate_list_page_request(huxiu_hash_code, 2)
            )

        return request_list

    def _generate_list_page_request(self, huxiu_hash_code, page):
        return FormRequest(
            url=self.article_list_url,
            formdata={
                'huxiu_hash_code': huxiu_hash_code,
                'page': str(page)
            },
            meta={
                'huxiu_hash_code': huxiu_hash_code,
                'page': page
            },
            callback=self.parse_list
        )

    def parse_list(self, response):
        request_list = []

        result = json.loads(response.body)

        total_page = result['total_page']

        data = result['data']
        aid_list = re.findall('data-aid\s*=\s*"(\d+)"', data)

        if aid_list:
            request_list.extend(self._generate_news_page_requests(aid_list))

        page = response.meta['page']
        if page < total_page:
            request_list.append(
                self._generate_list_page_request(
                    response.meta['huxiu_hash_code'],
                    page + 1
                )
            )

        return request_list

    def parse_news(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="article-wrap"]/h1', MapCompose(text))
        l.add_xpath('content', '//*[@id="article_content"]',
                    MapCompose(safe_html), Join('\n'))

        l.add_xpath('author',
                    '//*[@class="author-name"]',
                    MapCompose(text))

        l.add_xpath('publish_time',
                    '//*[@class="article-time"]',
                    MapCompose(
                        PipelineProcessor(
                            text,
                            DateProcessor('%Y-%m-%d %H:%M')
                        )
                    ))

        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))

        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))

        l.add_value('source_domain', 'huxiu.com')
        l.add_value('source_name', u'虎嗅网')

        i = l.load_item()
        return i
