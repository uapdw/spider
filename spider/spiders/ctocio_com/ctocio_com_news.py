# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CtocioNewsSpider(NewsSpider):

    u"""IT经理网新闻爬虫"""

    name = 'ctocio_com_news'
    allowed_domains = ['ctocio.com']
    start_urls = ['http://www.ctocio.com/']

    target_urls = [
        'ctocio\.com/ccnews/\d+\.html'
    ]

    title_xpath = '//*[@class="post"]/h1'
    content_xpath = '//*[@class="entrys"]'
    author_xpath = '//*[@rel="author"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="postinfo"]/li[2]'
    publish_time_re = u'.*,\s*(\S{1,2})月\s*(\d{1,2})\s*,\s*(\d{4}).*'
    publish_time_re_join = '-'
    publish_time_format = '%m-%d-%Y'

    source_domain = 'ctocio.com'
    source_name = u'IT经理网'

    month_dict = {
        u'一': 1,
        u'二': 2,
        u'三': 3,
        u'四': 4,
        u'五': 5,
        u'六': 6,
        u'七': 7,
        u'八': 8,
        u'九': 9,
        u'十': 10,
        u'十一': 11,
        u'十二': 12
    }

    def publish_time_filter(self, publish_time):
        splits = publish_time.split('-')
        month = splits[0]
        if month in self.month_dict:
            splits[0] = str(self.month_dict[month])
        return '-'.join(splits)
