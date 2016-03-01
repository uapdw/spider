# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import IFengNewsLoader


class IFengAutoHangyeSpider(LoaderMappingSpider):

    u"""凤凰汽车行业爬虫"""

    name = 'ifeng_com_auto_hangye'
    allowed_domains = ['auto.ifeng.com']
    start_urls = ['http://auto.ifeng.com/hangye/']

    #target_urls = [
    #    'auto\.ifeng\.com/hangye/\d{1}.shtml',#文章列表翻页
    #
    #    #'auto\.ifeng\.com/\S+?/\d{8}/\d{1,}.shtml'#文章
    #    'auto\.ifeng\.com/xinwen/\d{8}/\d{1,}.shtml',#文章
    #    'auto\.ifeng\.com/pinglun/\d{8}/\d{1,}.shtml',#文章
    #    'auto\.ifeng\.com/fangtan/\d{8}/\d{1,}.shtml',#文章
    #    'auto\.ifeng\.com/baogao/\d{8}/\d{1,}.shtml',#文章
    #    'auto\.ifeng\.com/hangye/zhuanlan/\d{8}/\d{1,}.shtml'#文章
    #]

    mapping = {
        'auto\.ifeng\.com/xinwen/\d{8}/\d{1,}.shtml': IFengNewsLoader,
        'auto\.ifeng\.com/pinglun/\d{8}/\d{1,}.shtml': IFengNewsLoader,
        'auto\.ifeng\.com/fangtan/\d{8}/\d{1,}.shtml': IFengNewsLoader,
        'auto\.ifeng\.com/baogao/\d{8}/\d{1,}.shtml': IFengNewsLoader,
        'auto\.ifeng\.com/hangye/zhuanlan/\d{8}/\d{1,}.shtml': IFengNewsLoader
    }
