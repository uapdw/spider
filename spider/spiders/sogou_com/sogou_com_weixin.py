# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.items import UradarNewsItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      safe_html)


class SogouWeixinSpider(CrawlSpider):

    u"""搜狗微信爬虫"""

    name = 'sogou_com_weixin'

    allowed_domains = [
        'weixin.sogou.com',
        'mp.weixin.qq.com'
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//*[@class="results"]//*[@class="txt-box"]\
                                 //a[contains(@id, "sogou")]')
            ),
            callback='parse_weixin'
        ),
        Rule(
            LinkExtractor(
                allow=('.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//*[@id="sogou_next"]')
            )
        ),
    )

    def __init__(self, keyword=None, *args, **kwargs):
        super(SogouWeixinSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://weixin.sogou.com/weixin?type=2&query=%s' % keyword
        ]

    def parse_weixin(self, response):

        l = ItemLoader(item=UradarNewsItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="rich_media_title"]',
                    MapCompose(text))

        l.add_xpath('content', '//*[@class="rich_media_content "]',
                    MapCompose(safe_html), Join('\n'))

        l.add_xpath('author',
                    '//*[@class="rich_media_meta rich_media_meta_text"][2]',
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
                    '//*[@class="rich_media_meta rich_media_\
                    meta_link rich_media_meta_nickname"]',
                    MapCompose(text))

        l.add_xpath('abstract', '//meta[@name="description"]/@content',
                    MapCompose(text))

        l.add_xpath('keywords', '//meta[@name="keywords"]/@content',
                    MapCompose(text))

        l.add_value('source_domain', 'sogou.com')
        l.add_value('source_name', u'搜狗')

        i = l.load_item()
        return i
