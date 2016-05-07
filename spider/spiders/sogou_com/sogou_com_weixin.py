# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.items import UradarWeixinItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      SafeHtml)


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
                restrict_xpaths=('//div[@id="page-content"]')
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
        Rule(
            LinkExtractor(
                allow=('.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//div[@class="wx-news-info2"]')
            )
        ),
        Rule(
            LinkExtractor(
                allow=('mp\.weixin\.qq\.com\/profile.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//div[@class="weui_msg_card_list"]')
            )
        ),
    )

    def __init__(self, keyword=None, *args, **kwargs):
        super(SogouWeixinSpider, self).__init__(*args, **kwargs)
        for i in range(0, 20):
            self.start_urls.append('http://weixin.sogou.com/pcindex/pc/pc_%s/pc_%s.html' % (i, i))
            for page in range(1,16):
                self.start_urls.append('http://weixin.sogou.com/pcindex/pc/pc_%s/%s.html' % (i, page))
        #self.start_urls = [
        #    #'http://weixin.sogou.com/weixin?type=2&query=%s' % keyword
        #]

    def parse_weixin(self, response):

        l = ItemLoader(item=UradarWeixinItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', '//*[@class="rich_media_title"]',
                    MapCompose(text))

        l.add_xpath('content', '//*[@class="rich_media_content "]',
                    MapCompose(SafeHtml(response.url)), Join('\n'))

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

        l.add_value('site_domain', 'sogou.com')
        l.add_value('site_name', u'搜狗')

        i = l.load_item()
        return i
