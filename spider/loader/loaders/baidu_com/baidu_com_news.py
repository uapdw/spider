# -*- coding: utf-8 -*-

from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.selector import Selector
from spider.loader import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor, PipelineProcessor,
                                      white_space)
from spider.items import UradarNewsItem
# from urllib import quote
import re
import datetime


class BaiduNewsLoader:
    u"""百度新闻爬虫"""
    
#     url_xpath = '//h3[@class="c-title"]/a/@href'
    publish_time_xpath = '//p[@class="c-author"]'
    publish_time_re = u'(?:\S+\s+(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+)|\S+\s+(.*))'
    publish_time_format = u'%Y%m%d%H%M'

    site_domain = 'autohome.com.cn'

    def load(self, response):
        sel = Selector(response)

        sites = sel.xpath("//div[@class='result']")
        reHtml = re.compile('</?\w+[^>]*>')
        reP = re.compile('<\s*p[^>]*>[^<]*<\s*/\s*p\s*>',re.I)
        reA = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>',re.I)
        items = []

        for site in sites:
            title = []
            siteName = []
#             postTime = []
            content = []
            titleStr = site.xpath("h3/a").extract()
            url = site.xpath("h3/a/@href").extract()
            title.append(reHtml.sub('',titleStr[0]))
            siteStr = site.xpath("div[@class='c-summary c-row c-gap-top-small']/div[@class='c-span18 c-span-last']/p[@class='c-author']/text()").extract()
            if len(siteStr) < 1:
                siteStr = site.xpath("div[@class='c-summary c-row ']/p[@class='c-author']/text()").extract()

            siteStrList = siteStr[0].replace(u'\xa0',u' ').split(' ')
            siteName.append(siteStrList[0])
            detailStr = site.xpath("div[@class='c-summary c-row ']").extract()
            if len(detailStr) < 1:
                detailStr = site.xpath("div[@class='c-summary c-row c-gap-top-small']").extract()
            detail = reP.sub('',detailStr[0])
            detail = reA.sub('',detail)
            content.append(reHtml.sub('',detail))

#           postTime.append(datetime.datetime.strptime(siteStrList[2].replace(u'年',u'-').replace(u'月',u'-').replace(u'日',u''),u'%Y-%m-%d'))
            l = ItemLoader(item=UradarNewsItem(), response=response)
            l.default_output_processor = TakeFirst()
            l.add_value('title',title)
            l.add_value('site_name',siteName)
            l.add_value('content',content)
            l.add_value('add_time',datetime.datetime.now())
            l.add_value('url', url)

            processor_list = [text]

            processor_list.append(DateProcessor(self.publish_time_format))

            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(
                            PipelineProcessor(
                                text,
                                self.filter_publish_time,
                                DateProcessor(self.publish_time_format)
                            )
                        ))
            items.append(l.load_item())

        return items
    
    
    def filter_publish_time(self, text):
        match = re.match(u'\S+\s+(\d+)年(\d+)月(\d+)日\s*(\d+):(\d+)', text)
        if match:
            return ''.join(match.groups())
        
        match = re.match('\S+\s+(.*)', text)
        if match:
            return match.group(1)
        
        return ''
