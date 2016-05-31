# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.items import UradarWeixinItem
from spider.loader.processors import (text, DateProcessor, PipelineProcessor,
                                      SafeHtml)


class SogouWeixinSearchSpider(CrawlSpider):

    u"""搜狗微信搜索爬虫"""

    name = 'sogou_com_weixin_search'

    allowed_domains = [
        'weixin.sogou.com',
        'mp.weixin.qq.com'
    ]

    keywords = [
        u'章源钨业',
        u'有色金属'
    ]

    search_article_pattern = u'http://weixin.sogou.com/weixin?query={}&type=2'
    search_profile_pattern = u'http://weixin.sogou.com/weixin?query={}&type=1'

    start_urls = []
    for keyword in keywords:
        start_urls.append(search_article_pattern.format(keyword))
        start_urls.append(search_profile_pattern.format(keyword))

    rules = (
        Rule(
            LinkExtractor(
                allow=('weixin\.sogou\.com/weixin\?query=\S+&type=2.*'),
                allow_domains=allowed_domains
            )
        ),
        Rule(
            LinkExtractor(
                allow=('weixin\.sogou\.com/weixin\?query=\S+&type=1.*'),
                allow_domains=allowed_domains
            )
        ),
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
            callback='parse_weixin'
        )
    )

    def parse_weixin(self, response):

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
