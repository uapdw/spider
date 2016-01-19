# -*- coding: utf-8 -*-

import datetime

from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor, PipelineProcessor)
from spider.items import UradarNewsItem, UradarBlogItem


class NewsLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'content_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    title_xpath = '//title'
    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)), Join('\n'))

        # author可选
        auther_xpath = getattr(self, 'author_xpath', None)
        if auther_xpath is not None:
            auther_re = getattr(self, 'author_re', None)
            if auther_re is None:
                l.add_xpath('author', self.author_xpath, MapCompose(text))
            else:
                l.add_xpath('author', self.author_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选

        processor_list = [text]

        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is not None:
            processor_list.append(
                RegexProcessor(
                    publish_time_re,
                    join_str=getattr(self, 'publish_time_re_join', u'')
                )
            )

        publish_time_filter = getattr(self, 'publish_time_filter', None)
        if publish_time_filter is not None:
            processor_list.append(
                publish_time_filter
            )

        processor_list.append(DateProcessor(self.publish_time_format))

        l.add_xpath('publish_time', self.publish_time_xpath,
                    MapCompose(
                        PipelineProcessor(
                            *processor_list
                        )
                    ))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source可选
        source_xpath = getattr(self, 'source_xpath', None)
        if source_xpath:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i


class BlogLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'title_xpath',
        'content_xpath',
        'author_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarBlogItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)))

        # author_re可选
        auther_re = getattr(self, 'author_re', None)
        if auther_re is None:
            l.add_xpath('author', self.author_xpath, MapCompose(text))
        else:
            l.add_xpath('author', self.author_xpath, MapCompose(text),
                        MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选
        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is None:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   DateProcessor(self.publish_time_format))))
        else:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   RegexProcessor(publish_time_re),
                                   DateProcessor(self.publish_time_format))))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source_re可选
        if getattr(self, 'source_xpath', None) is not None:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i


class It168NewsLoader(NewsLoader):

    u"""It168新闻爬虫"""

    name = 'it168_com_news'
    allowed_domains = ['it168.com']
    start_urls = ['http://www.it168.com/']

    target_urls = [
        'it168\.com/a\d{4}/\d{4}/\d+/\d+\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="detailWord"]'
    author_xpath = '//*[@class="time"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="time"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*(\S+).*'

    source_domain = 'it168.com'
    source_name = 'It168'


class DataTsciComCnNewsLoader(NewsLoader):

    u"""深度数据新闻爬虫"""

    name = 'data_tsci_com_cn_news'
    allowed_domains = ['data.tsci.com.cn']
    start_urls = ['http://data.tsci.com.cn/']

    target_urls = [
        'data\.tsci\.com\.cn/News/HTM/\d{8}/\d+.htm',
        'data\.tsci\.com\.cn/News/NewsShow\.aspx\?NewsId=\d+'
    ]

    title_xpath = '//*[@class="NewsTit"]'
    content_xpath = '//*[@class="NewsCon"]'
    publish_time_xpath = '//*[@class="NewsSouce"]'
    publish_time_re = u'.*(\d{4}/\d{2}/\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y/%m/%d %H:%M'
    source_xpath = '//*[@class="NewsSouce"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'data.tsci.com.cn'
    source_name = u'深度数据'


class QudongNewsLoader(NewsLoader):

    u"""驱动中国新闻爬虫"""

    name = 'qudong_com_news'
    allowed_domains = ['qudong.com']
    start_urls = ['http://www.qudong.com/']

    target_urls = [
        'qudong\.com/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="art-hd"]/h1'
    content_xpath = '//*[@class="content"]'
    publish_time_xpath = '//*[@id="pubtime"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="art-hd"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'qudong.com'
    source_name = u'驱动中国'


class Kn58NewsLoader(NewsLoader):

    u"""微客网新闻爬虫"""

    name = 'kn58_com_news'
    allowed_domains = ['kn58.com']
    start_urls = ['http://www.kn58.com/']

    target_urls = [
        'kn58\.com/.*/detail_\d{4}_\d{4}/\d+\.html'
    ]

    title_xpath = '//*[@class="title"]/h1'
    content_xpath = '//*[@class="left"]'
    publish_time_xpath = '//*[@class="titiefu"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="titiefu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'kn58.com'
    source_name = u'微客网'


class CSDNNewsLoader(NewsLoader):

    u"""CSDN新闻爬虫"""

    name = 'csdn_net_news'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    target_urls = [
        'article/\d{4}-\d{2}-\d{2}/\d+'
    ]

    title_xpath = '//h1[@class="title"]'
    content_xpath = '//div[@class="content"]/div[@class="left"]\
                     /div[@class="detail"]/div[@class="con news_content"]'
    author_xpath = '//*[@class="tit_bar"]'
    author_re = u'.*?作者\s*(\S+).*'
    publish_time_xpath = '//*[@class="tit_bar"]'
    publish_time_re = u'.*?发表于\s*(\d+-\d+-\d+ \d+:\d+|\S+).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="tit_bar"]'
    source_re = u'.*?来源\s*(\S+)\|.*'

    source_domain = 'csdn.net'
    source_name = 'CSDN'


class CSDNBlogLoader(BlogLoader):

    u"""CSDN博客爬虫"""

    name = 'csdn_net_blog'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    target_urls = [
        'http://blog.csdn.net/\S+?/article/details/\d+'
    ]

    title_xpath = '//*[@class="link_title"]'
    content_xpath = '//div[@class="article_content"]'
    author_xpath = '//*[@class="user_name"]'
    publish_time_xpath = '//*[@class="link_postdate"]'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_domain = 'csdn.net'
    source_name = 'CSDN'


class TechwebNewsLoader(NewsLoader):

    u"""TechWeb新闻爬虫"""

    name = 'techweb_com_cn_news'
    allowed_domains = ['techweb.com.cn']
    start_urls = ['http://www.techweb.com.cn/']

    target_urls = [
        'www\.techweb\.com\.cn/\S+/\d{4}-\d{2}-\d{2}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="content_txt"]'
    author_xpath = '//*[@class="author"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="date"]'
    publish_time_format = '%Y.%m.%d %H:%M:%S'
    source_xpath = '//*[@class="where"]'
    source_re = u'.*?来源:\s*(\S+).*'

    source_domain = 'techweb.com.cn'
    source_name = 'TechWeb'


class CnsoftNewsLoader(NewsLoader):

    u"""中国软件资讯网新闻爬虫"""

    name = 'cnsoftnews_com_news'
    allowed_domains = ['cnsoftnews.com']
    start_urls = ['http://www.cnsoftnews.com/']

    target_urls = [
        'http://www.cnsoftnews.com/\w+/\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="content_info"]'
    author_xpath = '//*[@class="article"]/b'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@class="article"]/b'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@class="article"]/b'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'cnsoftnews.com'
    source_name = u'中国软件资讯网'


class CtocioNewsLoader(NewsLoader):

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


class N199itNewsLoader(NewsLoader):

    u"""199it新闻爬虫"""

    name = '199it_com_news'
    allowed_domains = ['199it.com']
    start_urls = ['http://www.199it.com/']

    target_urls = [
        '199it\.com/archives/\d+\.html'
    ]

    title_xpath = '//*[@class="entry-title"]'
    content_xpath = '//*[@class="entry-content"]'
    publish_time_xpath = '//*[@class="search-post-info-table"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{1,2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = '199it.com'
    source_name = '199it'


class QQNewsLoader(NewsLoader):

    u"""腾讯新闻爬虫"""

    name = 'qq_com_news'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com']

    target_urls = [
        'news.qq.com/a/\d{8}/\d+.htm'
    ]

    title_xpath = '//*[@class="hd"]/h1'
    content_xpath = '//*[@id="C-Main-Article-QQ"]/*[@class="bd"]'
    author_xpath = '//*[@class="color-a-3"]'
    publish_time_xpath = '//*[@class="article-time"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="color-a-1"]/a'
    abstract_xpath = '//meta[@name="Description"]/@content'

    source_domain = 'qq.com'
    source_name = u'腾讯网'


class CniiComCnNewsLoader(NewsLoader):

    u"""中国信息产业网新闻爬虫"""

    name = 'cnii_com_cn_news'
    allowed_domains = ['cnii.com.cn']
    start_urls = ['http://www.cnii.com.cn/']

    target_urls = [
        'http://www.cnii.com.cn/\w+/\d{4}-\d{2}/\d+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="conzw"]'
    author_xpath = '//*[@class="conzz"]'
    author_re = u'.*?作者：(.*).*'
    publish_time_xpath = '//*[@class="conzz"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="conzz"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'cnii.com.cn'
    source_name = u'中国信息产业网'


class LeiphoneNewsLoader(NewsLoader):

    u"""雷锋网新闻爬虫"""

    name = 'leiphone_com_news'
    allowed_domains = ['leiphone.com']
    start_urls = ['http://www.leiphone.com/']

    target_urls = [
        'leiphone\.com/news/\d{6}/\S+\.html'
    ]

    title_xpath = '//*[@class="pageTop"]/h1'
    content_xpath = '//*[contains(@class, "pageCont")]'
    author_xpath = '//*[@class="pi-author"]'
    author_re = u'.*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*\S+\s*(\S+).*'
    publish_time_xpath = '//*[@class="pi-author"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="pi-author"]'
    source_re = u'.*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*(\S+)\s*\S+.*'

    source_domain = 'leiphone.com'
    source_name = u'雷锋网'


class ZolNewsLoader(NewsLoader):

    u"""中关村在线新闻爬虫"""

    name = 'zol_com_cn_news'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://www.zol.com.cn/']

    target_urls = [
        'zol\.com\.cn/\d+/\d+\.html'
    ]

    title_xpath = '//*[contains(@class, "article-header") or \
                  @class="article-tit"]/h1'
    content_xpath = '//*[@id="article-content"]'
    author_xpath = '//*[@class="editor"]'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?\[\s*(.*)\s*\].*'

    source_domain = 'zol.com.cn'
    source_name = u'中关村在线'


class EworksNewsLoader(NewsLoader):

    u"""e-works新闻爬虫"""

    name = 'eworks_net_cn_news'
    allowed_domains = ['e-works.net.cn']
    start_urls = ['http://www.e-works.net.cn/']

    target_urls = [
        'http://\w+.e-works.net.cn/\w+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//div[@class="mt15 f14 lh240 WaresDetail"]'
    author_xpath = '//div[@class="fl mt10"]'
    author_re = u'.*?作者：(.*)关键字：.*'
    publish_time_xpath = '//div[@class="fl mt10" or @class="fl mt10 pb10"]'
    publish_time_re = u'.*(\d{4})[年|/](\d{1,2})[月|/](\d{1,2}).*'
    publish_time_format = '%Y%m%d'
    source_xpath = '//div[@class="fl mt10"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'e-works.net.cn'
    source_name = u'e-works'


class SootooNewsLoader(NewsLoader):

    u"""速途网新闻爬虫"""

    name = 'sootoo_com_news'
    allowed_domains = ['sootoo.com']
    start_urls = ['http://www.sootoo.com/']

    target_urls = [
        'http://www.sootoo.com/content/\d+.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="content"]'
    author_xpath = '//*[@class="t11_info"]'
    author_re = u'.*?作者:\s*(.*)\s*发布.*'
    publish_time_xpath = '//*[@class="t11_info"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@class="t11_info"]'
    source_re = u'.*?来源:\s*(\S+).*'

    source_domain = 'sootoo.com'
    source_name = u'速途网'


class VsharingNewsLoader(NewsLoader):

    u"""畅享网新闻爬虫"""

    name = 'vsharing_com_news'
    allowed_domains = ['vsharing.com']
    start_urls = ['http://www.vsharing.com/']

    target_urls = [
        'http://www.vsharing.com/\w+/\w+/\d{4}-\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="content_art"]'
    author_xpath = '//div[@class="summary_author"]/div/div'
    author_re = u'.*?作者：\s*\S+\s+(.*).*'
    publish_time_xpath = '//*[@class="summary_author"]'
    publish_time_re = u'.*(\d{4})/(\d{2})/(\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//div[@class="summary_author"]/div/div/span'
#     source_re = u'.*?来源：(\S+).*'

    source_domain = 'vsharing.com'
    source_name = u'畅享网'


class PeopleComCnNewsLoader(NewsLoader):

    u"""人民网新闻爬虫"""

    name = 'people_com_cn_news'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://www.people.com.cn/']

    target_urls = [
        'people\.com\.cn/n/\d{4}/\d{4}/c\d+-\d+.html'
    ]

    title_xpath = '//*[@id="p_title"]'
    content_xpath = '//*[@id="p_content"]'
    author_xpath = '//*[@class="author"]'
    publish_time_xpath = '//*[@id="p_publishtime"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@id="p_origin"]'
    source_re = u'.*?来源\s*(\S+).*'

    source_domain = 'people.com.cn'
    source_name = u'人民网'


class WWW163NewsLoader(NewsLoader):

    u"""网易新闻爬虫"""

    name = '163_com_news'
    allowed_domains = ['163.com']
    start_urls = ['http://www.163.com/']

    target_urls = [
        '\S+\.163.com/\d{2}/\d{4}/\d+/\S+.html'
    ]

    title_xpath = '//h1[@id="h1title"]'
    content_xpath = '//div[@class="end-text"]'
    author_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[contains(@class, "ep-time-soure")]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = '163.com'
    source_name = u'网易'


class ZJOLComCnNewsLoader(NewsLoader):
    '''浙江在线新闻爬虫'''

    name = 'zjol_com_cn_news'
    allowed_domains = ['zjol.com.cn']
    start_urls = ['http://www.zjol.com.cn/']

    target_urls = [
        '\w+\.zjol.com.cn/\w+/\d{4}/\d{2}/\d{2}/\d+.shtml'
    ]

    title_xpath = '//div[@class="contTit" or @class="artTitle"]'
    content_xpath = '//div[@class="contTxt"]'
    author_xpath = '//span[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//span[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'zjol.com.cn'
    source_name = '浙江在线'


class IdcNewsLoader(NewsLoader):

    u"""idc新闻爬虫"""

    name = 'idc_com_cn_news'
    allowed_domains = ['idc.com.cn']
    start_urls = ['http://www.idc.com.cn/']

    target_urls = [
        'idc\.com\.cn/about/press\.jsp\?id=\S+'
    ]

    title_xpath = '//*[@class="bodybkbd"]'
    content_xpath = '//*[@class="bodybk"]'
    publish_time_xpath = '//*[@class="bodybk"]'
    publish_time_re = u'.*日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="bodybk"]'
    source_re = u'.*信息来源：\s*(\S+).*'

    source_domain = 'idc.com.cn'
    source_name = 'IDC'


class EastDayNewsLoader(NewsLoader):
    '''东方网新闻爬虫'''

    name = 'eastday_com_news'
    allowed_domains = ['eastday.com']
    start_urls = ['http://www.eastday.com/']

    target_urls = [
        '\w+\.eastday.com/\w+/\d{8}/\w+.html'
    ]

    title_xpath = '//*[@id="biaoti"]'
    content_xpath = '//*[@id="zw"]'
    author_xpath = '//*[@class="time grey12a fc lh22"]'
    author_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}.*作者:(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@class="time grey12a fc lh22"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*来源:(\S+).*'

    source_domain = 'eastday.com'
    source_name = '东方网'


class CaijingNewsLoader(NewsLoader):

    u"""财经网新闻爬虫"""

    name = 'caijing_com_cn_news'
    allowed_domains = ['caijing.com.cn']
    start_urls = ['http://www.caijing.com.cn/']

    target_urls = [
        'caijing\.com\.cn/\d{8}/\d+\.shtml'
    ]

    title_xpath = '//*[@id="cont_title"]'
    content_xpath = '//*[@id="the_content"]'
    author_xpath = '//*[@id="editor_baidu"]'
    author_re = u'.*?编辑：\s*(\S+)\).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'

    source_domain = 'caijing.com.cn'
    source_name = u'财经网'


class CcidnetNewsLoader(NewsLoader):

    u"""赛迪网新闻爬虫"""

    name = 'ccidnet_com_news'
    allowed_domains = ['ccidnet.com']
    start_urls = ['http://www.ccidnet.com/']

    target_urls = [
        'ccidnet\.com/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//h2'
    content_xpath = '//*[@class="main_content"]'
    author_xpath = '//*[@class="tittle_j"]'
    author_re = u'.*?（作者：\S+?）.*'
    publish_time_xpath = '//*[@class="tittle_j"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="tittle_j"]'
    source_re = u'.*?（来源：\S+?）.*'

    source_domain = 'ccidnet.com'
    source_name = u'赛迪网'


class ChinabyteNewsLoader(NewsLoader):

    u"""搜狐新闻爬虫"""

    name = 'chinabyte_com_news'
    allowed_domains = ['chinabyte.com']
    start_urls = ['http://chinabyte.com/']

    target_urls = [
        'chinabyte\.com/\d+/\d+\.shtml'
    ]

    title_xpath = '//*[@id="artibodyTitle"]'
    content_xpath = '//*[@id="main-article"]'
    author_xpath = '//*[@class="auth"]'
    publish_time_xpath = '//*[@class="date"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="where"]'

    source_domain = 'chinabyte.com'
    source_name = u'比特网'


class CiotimesNewsLoader(NewsLoader):

    u"""CIO时代新闻爬虫"""

    name = 'ciotimes_com_news'
    allowed_domains = ['ciotimes.com']
    start_urls = ['http://www.ciotimes.com/']

    target_urls = [
        'ciotimes\.com/\S+/\d+\.html'
    ]

    title_xpath = '//*[contains(@class, "zw")]/h4[1]'
    content_xpath = '//*[contains(@class, "zw")]'
    publish_time_xpath = '//*[contains(@class, "ly")]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[contains(@class, "ly")]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ciotimes.com'
    source_name = u'CIO时代'


class XinhuanetNewsLoader(NewsLoader):

    u"""新华网新闻爬虫"""

    name = 'xinhuanet_com_news'
    allowed_domains = ['xinhuanet.com']
    start_urls = ['http://xinhuanet.com/']

    target_urls = [
        'news\.xinhuanet\.com/\S+/\d{4}-\d{2}/\d{2}/c_\d+.htm'
    ]

    title_xpath = '//*[@id="title"]'
    content_xpath = '//*[@class="article" or @class="news_con" or \
                     @id="content"]'
    author_xpath = '//*[@class="editor" or @id="editblock"]'
    author_re = u'.*?编辑: \s*(\S+).*'
    publish_time_xpath = '//*[@class="time" or @id="pubtimeandfrom" or \
                          @id="pubtime"]'
    publish_time_re = u'.*?(\d{4})[年|-](\d{2})[月|-](\d{2}).*?\
                        (\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//*[@class="source" or @id="from" or @id="source"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'xinhuanet.com'
    source_name = u'新华网'


class ChinaComCnNewsLoader(NewsLoader):

    u"""中国网新闻爬虫"""

    name = 'china_com_cn_news'
    allowed_domains = ['china.com.cn']
    start_urls = ['http://www.china.com.cn/']

    target_urls = [
        'china\.com\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm',
        'china\.com\.cn/.*/\d{8}/\d+\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="artbody" or @id="fontzoom" or \
                    @class="content" or @class="Content"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'china.com.cn'
    source_name = u'中国网'


class PcpopNewsLoader(NewsLoader):

    u"""泡泡网新闻爬虫"""

    name = 'pcpop_com_news'
    allowed_domains = ['pcpop.com']
    start_urls = ['http://www.pcpop.com/']

    target_urls = [
        'pcpop\.com/doc/\d+/\d+/\d+\.shtml'
    ]

    title_xpath = '//*[@class="l1"]/h1'
    content_xpath = '//*[@class="main"]'
    author_xpath = '//*[@class="chuchu"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="chuchu"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="chuchu"]'
    source_re = u'.*?出处：\s*(\S+).*'

    source_domain = 'pcpop.com'
    source_name = u'泡泡网'


class SapNewsLoader(NewsLoader):

    u"""SAP新闻爬虫"""

    name = 'sap_com_news'
    allowed_domains = ['global.sap.com']
    start_urls = [
        'http://global.sap.com/china/news-reader/index.epx'
    ]

    target_urls = [
        '.*china/news-reader/index\.epx\?.*articleID=\d+.*'
    ]

    title_xpath = '//head/title[1]'
    content_xpath = '//*[@id="articledisplay"]'
    publish_time_xpath = '//*[@class="articledate"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="articlesource"]'

    source_domain = 'sap.com'
    source_name = 'SAP'


class SPNComNewsLoader(NewsLoader):

    u"""睿商在线新闻爬虫"""

    name = 'spn_com_cn_news'
    allowed_domains = ['spn.com.cn']
    start_urls = ['http://www.spn.com.cn/']

    target_urls = [
        'http://www.spn.com.cn/\w+/\d+/\d+.html'
    ]

    title_xpath = '//*[@class="hei20"]'
    content_xpath = '//*[@class="h14"]'
    author_xpath = '//*[@align="center" and @class="hui12"]'
    author_re = u'.*?\S+\s+\S+\s+(\S+).*'
    publish_time_xpath = '//*[@align="center" and @class="hui12"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日.*'
    publish_time_format = '%Y%m%d'
    source_xpath = '//*[@align="center" and @class="hui12"]'
    source_re = u'.*?\S+\s+(\S+)\s+.*'

    source_domain = 'spn.com.cn'
    source_name = u'睿商在线'


class ENorthNewsLoader(NewsLoader):
    '''北方网新闻爬虫'''

    name = 'enorth_com_cn_news'
    allowed_domains = ['enorth.com.cn']
    start_urls = ['http://www.enorth.com.cn/']

    target_urls = [
        '\w+\.enorth.com.cn/\w+/\d{4}/\d{2}/\d{2}/|w+.shtml'
    ]

    title_xpath = '//*[@class="title heiti zi24 yanse1"]'
    content_xpath = '//*[@class="zi14 hanggao24"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'enorth.com.cn'
    source_name = '北方网'


class N100ecNewsLoader(NewsLoader):

    u"""中国电子商务研究中心新闻爬虫"""

    name = '100ec_cn_news'
    allowed_domains = ['100ec.cn']
    start_urls = ['http://www.100ec.cn']

    target_urls = [
        '100ec\.cn/detail--\d+\.html'
    ]

    title_xpath = '//*[@class="newsview"]/h2'
    content_xpath = '//*[@class="nr"]'
    publish_time_xpath = '//*[@class="public f_hong"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="public f_hong"]'
    source_re = u'.*?(\S+)\s*\d{4}年\d{2}月\d{2}日\d{2}:\d{2}.*'

    site_domain = '100ec.com'
    site_name = u'中国电子商务研究中心'


class CbinewsNewsLoader(NewsLoader):

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


class N36dsjNewsLoader(NewsLoader):

    u"""36dsj新闻爬虫"""

    name = '36dsj_com_news'
    allowed_domains = ['36dsj.com']
    start_urls = ['http://www.36dsj.com/']

    target_urls = [
        '36dsj\.com/archives/\d+'
    ]

    title_xpath = '//*[@class="article-title"]'
    content_xpath = '//*[@class="article-content"]'
    author_xpath = '//*[@class="article-meta"]/li[1]'
    # author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="article-meta"]/li[2]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="article-meta"]/li[3]'

    source_domain = '36dsj.com'
    source_name = u'36大数据'


class SinaNewsLoader(NewsLoader):

    u"""新浪新闻爬虫"""

    name = 'sina_com_cn_news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://www.sina.com.cn']

    target_urls = [
        '.*?sina\.com\.cn/\S+?/\d{4}-\d{2}-\d{2}/doc-\S+\.shtml',
        '.*?sina\.com\.cn/\d{4}-\d{2}-\d{2}/\d+.html',
        '.*?sina\.com\.cn/\S+?/\d{8}/\d+\.shtml'
    ]

    title_xpath = '//*[@id="artibodyTitle" or @id="main_title"]'
    content_xpath = '//*[@id="artibody"]'
    author_xpath = '//*[@class="show_author"]'
    author_re = u'.*?（编辑：\S+?）.*'
    publish_time_xpath = '//*[@id="pub_date" or @class="time-source"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@id="media_name" or @data-sudaclick="media_name"]'

    source_domain = 'sina.com.cn'
    source_name = u'新浪'


class YCWBNewsLoader(NewsLoader):
    '''金羊网新闻爬虫'''

    name = 'ycwb_com_news'
    allowed_domains = ['ycwb.com']
    start_urls = ['http://www.ycwb.com/']

    target_urls = [
        '\w+\.ycwb.com/\d{4}-\d{2}/\d+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="main_article"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?发表时间：(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源:(\S+).*'

    source_domain = 'ycwb.com'
    source_name = '金羊网'


class CbismbNewsLoader(NewsLoader):

    u"""中小企业IT网新闻爬虫"""

    name = 'cbismb_com_news'
    allowed_domains = ['cbismb.com']
    start_urls = ['http://cbismb.com/']

    target_urls = [
        'cbismb\.com/.*/news/\d{4}-\d{2}-\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@id="cont_title"]'
    content_xpath = '//*[@id="the_content"]'
    author_xpath = '//*[@class="textsource"]'
    author_re = u'.*?作者：\s*(\S+)\s*责任编辑.*'
    publish_time_xpath = '//*[@class="textsource"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="textsource"]'
    source_re = u'.*?来源：\s*(\S+)\s*关键字.*'

    source_domain = 'cbismb.com'
    source_name = u'中小企业IT网'


class GmwNewsLoader(NewsLoader):

    u"""光明网新闻爬虫"""

    name = 'gmw_cn_news'
    allowed_domains = ['gmw.cn']
    start_urls = ['http://gmw.cn/']

    target_urls = [
        'gmw\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm'
    ]

    title_xpath = '//*[@id="articleTitle" or @class="picContentHeading"]'
    content_xpath = '//*[@id="contentMain" or @id="ArticleContent"]'
    author_xpath = '//*[@id="contentLiability"]'
    author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//*[@id="pubTime"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@id="source"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'gmw.cn'
    source_name = u'光明网'


class SohuNewsLoader(NewsLoader):

    u"""搜狐新闻爬虫"""

    name = 'sohu_com_news'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com/']

    target_urls = [
        '.*?sohu.com/\d{8}/n\d+.shtml'
    ]

    title_xpath = '//h1[@itemprop="headline"]'
    content_xpath = '//div[@itemprop="articleBody"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'sohu.com'
    source_name = u'搜狐'


class ChinaNewsLoader(NewsLoader):
    '''中华网新闻爬虫'''

    name = 'china_com_news'
    allowed_domains = ['china.com']
    start_urls = ['http://www.china.com/index.html']

    target_urls = [
        '\w+\.china.com/\w+/\w*/\d+/\d{8}/\d{8}_all.html'
    ]

    title_xpath = '//h1[@id="chan_newsTitle"]'
    content_xpath = '//div[@id="chan_newsDetail"]'
    author_xpath = '//div[@class="editor"]'
    author_re = u'.*?\(责任编辑：(\S+)\).*'
    publish_time_xpath = '//div[@id="chan_newsInfo"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//div[@id="chan_newsInfo"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*(\S+)\s*参与评论.*'

    source_domain = 'china.com'
    source_name = '中华网'


class CcwNewsLoader(NewsLoader):

    u"""计世网新闻爬虫"""

    name = 'ccw_com_cn_news'
    allowed_domains = ['ccw.com.cn']
    start_urls = ['http://www.ccw.com.cn/']

    target_urls = [
        'http://www.ccw.com.cn/article/view/\d+'
    ]

    title_xpath = '//div[@class="hd"]/h1'
    content_xpath = '//*[@class="bd"]'
    author_xpath = '//*[@class="author"]'
    author_re = u'.*?(.*)-.*'
    publish_time_xpath = '//*[@class="author"]'
    publish_time_re = u'.*(\d{4}).(\d{2}).(\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'

    source_domain = 'ccw.com.cn'
    source_name = u'计世网'


class CqNewsNetNewsLoader(NewsLoader):

    u"""华龙网新闻爬虫"""

    name = 'cqnews_net_news'
    allowed_domains = ['cqnews.net']
    start_urls = ['http://www.cqnews.net/']

    target_urls = [
        'cq\.cqnews\.net/\S+/\d{4}-\d{2}/\d{2}/content_\d+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="main_text"]'
    publish_time_xpath = '//*[@class="jiange3"][1]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="jiange3"][2]/a'

    source_domain = 'cqnews.net'
    source_name = u'华龙网'


class ChinaCloudNewsLoader(NewsLoader):

    u"""中云网新闻爬虫"""

    name = 'china-cloud_com_news'
    allowed_domains = ['china-cloud.com']
    start_urls = ['http://www.china-cloud.com/']

    target_urls = [
        'china-cloud\.com/.*/\d{8}_\d+\.html'
    ]

    title_xpath = '//*[@class="wenzhang_top"]/h2'
    content_xpath = '//*[@class="zhengwen"]'
    author_xpath = '//*[@class="sm_arcinfo"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="sm_arcinfo"]'
    publish_time_re = u'.*时间：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="sm_arcinfo"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'china-cloud.com'
    source_name = u'中云网'


class YidonghuaNewsLoader(NewsLoader):

    u"""移动信息化新闻爬虫"""

    name = 'yidonghua_com_news'
    allowed_domains = ['yidonghua.com']
    start_urls = ['http://www.yidonghua.com']

    target_urls = [
        'yidonghua\.com/post/\d+\.html'
    ]

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@id="wrap-content"]/*[@class="content"]'
    publish_time_xpath = '//*[@class="meta_date"]'
    publish_time_re = '.*(\d{4}/\d{2}/\d{2}).*'
    publish_time_format = '%Y/%m/%d'

    source_domain = 'yidonghua.com'
    source_name = u'移动信息化'


class DataguruNewsLoader(NewsLoader):

    u"""炼数成金新闻爬虫"""

    name = 'dataguru_cn_news'
    allowed_domains = ['dataguru.cn']
    start_urls = ['http://dataguru.cn/']

    target_urls = [
        'dataguru\.cn/article-\d+-\d+\.html'
    ]

    title_xpath = '//*[@class="ph"]'
    content_xpath = '//*[@id="article_content"]'
    author_xpath = '//*[@class="xg1"]'
    author_re = u'.*?原作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="xg1"]'
    publish_time_re = '.*?(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="xg1"]'
    source_re = u'.*?来自: \s*(\S+).*'

    source_domain = 'dataguru.cn'
    source_name = u'炼数成金'


class S3d4NewsLoader(NewsLoader):

    u"""说三道四新闻爬虫"""

    name = 's3d4_cn_news'
    allowed_domains = ['s3d4.cn']
    start_urls = ['http://s3d4.cn/']

    target_urls = [
        's3d4\.cn/news/\d+'
    ]

    title_xpath = '//*[@id="left_box"]/h1'
    content_xpath = '//*[@class="articlecontent"]'
    publish_time_xpath = '//*[@class="timebox"]'
    publish_time_re = u'.*发布时间：\s*(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y/%m/%d %H:%M:%S'
    source_xpath = '//*[@class="timebox"]'
    source_re = u'.*?发布：\s*(\S+).*'

    source_domain = 's3d4.cn'
    source_name = u'说三道四'


class TopointNewsLoader(NewsLoader):

    u"""支点网新闻爬虫"""

    name = 'topoint_com_cn_news'
    allowed_domains = ['topoint.com.cn']
    start_urls = ['http://www.topoint.com.cn/']

    target_urls = [
        'http://www.topoint.com.cn/html/article/\d{4}/\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//div[@id="content"]'
    author_xpath = '//div[@class="other"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//div[@class="other"]'
    publish_time_re = u'.*?(\d{4}-\d{1,2}-\d{1,2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//div[@class="other"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'topoint.com.cn'
    source_name = u'支点网'


class CctimeNewsLoader(NewsLoader):

    u"""飞象网新闻爬虫"""

    name = 'cctime_com_news'
    allowed_domains = ['cctime.com']
    start_urls = ['http://www.cctime.com/']

    target_urls = [
        'cctime\.com/html/\d{4}-\d{1,2}-\d{1,2}/\d+\.htm'
    ]

    title_xpath = '//title'
    content_xpath = '//*[@class="art_content"]'
    author_xpath = '//*[@class="editor"]'
    author_re = u'.*?编\s*辑：\s*(\S+).*'
    publish_time_xpath = '//*[@class="dateAndSource"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}:\d{1,2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="dateAndSource"]'
    source_re = u'.*\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{1,2}\s*(\S+).*'

    source_domain = 'cctime.com'
    source_name = u'飞象网'


class ZdnetNewsLoader(NewsLoader):

    u"""至顶网新闻爬虫"""

    name = 'zdnet_com_cn_news'
    allowed_domains = ['zdnet.com.cn']
    start_urls = ['http://www.zdnet.com.cn']

    target_urls = [
        'zdnet\.com\.cn/.*/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="foucs_title" or @class="root_h1"]'
    content_xpath = '//*[@class="qu_ocn"]'
    author_xpath = '//*[@class="qu_zuo"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="qu_zuo"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="qu_zuo"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'zdnet.com.cn'
    source_name = u'至顶网'


class YnetNewsLoader(NewsLoader):

    u"""北青网新闻爬虫"""

    name = 'ynet_com_news'
    allowed_domains = ['ynet.com']
    start_urls = ['http://www.ynet.com/']

    target_urls = [
        'news\.ynet\.com/[\d\.]+/\d{4}/\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@class=" BSHARE_POP"]'
    content_xpath = '//*[@id="pzoom"]'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ynet.com'
    source_name = u'北青网'


class HexunNewsLoader(NewsLoader):

    u"""和讯新闻爬虫"""

    name = 'hexun_com_news'
    allowed_domains = ['hexun.com']
    start_urls = ['http://www.hexun.com/']

    target_urls = [
        'hexun\.com/\d{4}-\d{2}-\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@id="artibodyTitle"]/h1'
    content_xpath = '//*[@id="artibody"]'
    author_xpath = '//*[@id="arctTailMark"]/following::*'
    author_re = u'.*?（责任编辑：\s*(\S+)\s*.*）.*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'hexun.com'
    source_name = u'和讯网'


class YeskyComNewsLoader(NewsLoader):

    u"""天极网新闻爬虫"""

    name = 'yesky_com_news'
    allowed_domains = ['yesky.com']
    start_urls = ['http://www.yesky.com/']

    target_urls = [
        'yesky.com/\d+/\d+.shtml'
    ]

    title_xpath = '//*[@class="title"]/h1'
    content_xpath = '//*[@class="article"]'
    author_xpath = '//*[@class="editor"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="detail"]/span[2]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="detail"]/span[1]'

    source_domain = 'yesky.com'
    source_name = u'天极网'


class QianLongNewsLoader(NewsLoader):

    u"""千龙网新闻爬虫"""

    name = 'qianlong_com_news'
    allowed_domains = ['qianlong.com']
    start_urls = ['http://www.qianlong.com/']

    target_urls = [
        '\w+\.qianlong.com/\d{4}/\d{4}/\d{6}\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="article-content"]'
    author_xpath = '//*[@class="editor"]/span'
    publish_time_xpath = '//*[@class="pubDate"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M'
    source_xpath = '//*[@class="source"]'

    source_domain = 'qianlong.com'
    source_name = u'千龙网'


class IFengNewsLoader(NewsLoader):

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


class CeocioNewsLoader(NewsLoader):

    u"""经理世界网新闻爬虫"""

    name = 'ceocio_com_cn_news'
    allowed_domains = ['ceocio.com.cn']
    start_urls = ['http://www.ceocio.com.cn/']

    target_urls = [
        'ceocio\.com\.cn/.*/\d{4}-\d{2}-\d{2}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="news_title"]'
    content_xpath = '//*[@class="news_body"]'
    author_xpath = '//*[@class="news_from"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="news_from"]'
    publish_time_re = u'.*时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="news_from"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ceocio.com.cn'
    source_name = u'经理世界网'
