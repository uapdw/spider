# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.items import UradarWeixinItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      SafeHtml)


class SogouWeixinSearchStep2Spider(CrawlSpider):

    u"""搜狗微信搜索文章爬虫"""

    name = 'sogou_com_weixin_search_step2'

    allowed_domains = [
        'weixin.sogou.com',
        'mp.weixin.qq.com'
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('mp\.weixin\.qq\.com/profile.*'),
                allow_domains=allowed_domains
            )
        ),
        Rule(
            LinkExtractor(
                allow=('mp\.weixin\.qq\.com/s.*'),
                allow_domains=allowed_domains
            ),
            callback='parse_article'
        )
    )

    def start_requests(self):
        with open('profile_links', 'r') as f:
            for url in f.read().split('\n'):
                yield Request(url, callback=self.parse_profile)
        with open('article_links', 'r') as f:
            for url in f.read().split('\n'):
                yield Request(url, callback=self.parse_article)

    def parse_profile(self, response):
        article_extractor = LinkExtractor(
            allow=('mp\.weixin\.qq\.com/s.*'),
            allow_domains=self.allowed_domains
        )
        article_links = article_extractor.extract_links(response)
        for article_link in article_links:
            yield Request(article_link.url)

    def parse_article(self, response):

        l = ItemLoader(item=UradarWeixinItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="rich_media_title"]',
                    MapCompose(text))

        l.add_xpath('content', '//*[@class="rich_media_content "]',
                    MapCompose(SafeHtml(response.url)), Join('\n'))

        l.add_xpath('author',
                    '//*[@class="rich_media_meta_list"]/em[2]',
                    MapCompose(text))

        l.add_xpath('publish_time',
                    '//*[@class="rich_media_meta rich_media_meta_text"][1]',
                    MapCompose(
                        PipelineProcessor(
                            text,
                            DateProcessor('%Y-%m-%d')
                        )
                    ))

        l.add_xpath('source',
                    '//*[@class="rich_media_meta_list"]/a',
                    MapCompose(text))

        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))

        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))

        l.add_value('site_domain', 'sogou.com')
        l.add_value('site_name', u'搜狗')

        i = l.load_item()
        return i
