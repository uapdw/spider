# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader, MergeLoader


class IFengNewsLoader(MergeLoader):
    def __init__(self):
        super(IFengNewsLoader, self).__init__([
            IFengNewsLoader1(),
            IFengNewsLoader2(),
            IFengNewsLoader3(),
            IFengNewsLoader4()
        ])


class IFengNewsLoader1(NewsLoader):
    u"""凤凰新闻爬虫"""

    name = 'ifeng_com_news'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://www.ifeng.com']

    target_urls = [
        'ifeng\.com/\S+?/\d{8}/\d+_\d{1}.shtml',
        'ifeng\.com/\S+?/\d{4}/\d{4}/\d+.shtml'
    ]

    title_xpath = '//*[@id="artical_topic" or @class="tit01"]'
    content_xpath = '//*[@id="artical_real"]'
    author_xpath = '//*[@id="author_baidu" or @itemprop="author"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@itemprop="datePublished" or @class="time01"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@itemprop="publisher" or @id="source_baidu"]'

    source_domain = 'ifeng.com'
    source_name = u'凤凰网'


class IFengNewsLoader2(NewsLoader):
    u"""凤凰汽车新闻"""

    title_xpath = '//div[@class="arl-cont"]/h3'
    content_xpath = '//div[@class="arl-c-txt"]'
    publish_time_xpath = '//span[@class="ai-date d"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日\s(\d{2}:\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = u'%Y-%m-%d-%H:%M:%S'
    source_xpath = '//span[@class="ai-source d"]'
    source_re = u'.*?来源：\s*(\S+).*'
    author_xpath = '//span[@class="ai-author d"]'
    author_re = u'.*?作者：\s*(\S+).*'

    source_domain = 'ifeng.com'
    source_name = u'凤凰网'


class IFengNewsLoader3(NewsLoader):
    u"""凤凰汽车新闻"""

    title_xpath = '//h1'
    content_xpath = '//div[@id="artical_real"]'
    publish_time_xpath = '//span[@class="t_1"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日\s(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = u'%Y-%m-%d-%H:%M'
    source_xpath = '//span[@class="t_2"]'
    #source_re = u'.*?来源：\s*(\S+).*'
    source_re = u'.*?来源：(\S+)\s*作者：.*'
    author_xpath = '//span[@class="t_2"]/span'
    author_re = u'.*'

    source_domain = 'ifeng.com'
    source_name = u'凤凰网'

class IFengNewsLoader4(NewsLoader):
    u"""凤凰汽车自媒体"""

    title_xpath = '//h1'
    content_xpath = '//div[@class="article_con"]'
    publish_time_xpath = '//div[@class="dtime"]/span'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = u'%Y-%m-%d'
    #source_xpath = '//span[@class="t_2"]'
    #source_re = u'.*?来源：\s*(\S+).*'
    #source_re = u'.*?来源：(\S+)\s*作者：.*'
    author_xpath = '//div[@class="name"]'
    author_re = u'.*'

    source_domain = 'ifeng.com'
    source_name = u'凤凰网'
