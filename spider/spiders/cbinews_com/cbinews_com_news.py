# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CbinewsNewsSpider(NewsSpider):

    u"""电脑商情网新闻爬虫"""

    name = 'cbinews_com_news'
    allowed_domains = ['cbinews.com']
    start_urls = ['http://www.cbinews.com']

    target_urls = [
        'cbinews\.com/\S+/news/\d{4}-\d{2}-\d{2}/\d+\.htm'
    ]

    title_xpath = '//*[@id="cont_title"]'
    content_xpath = '//*[@id="the_content"]/p'
    author_xpath = '//*[@class="textsource"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="textsource"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="textsource"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'cbinews.com'
    source_name = u'电脑商情网'
