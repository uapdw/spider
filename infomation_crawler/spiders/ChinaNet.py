# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy import Spider,Request
class ScienceSpider(CrawlSpider):
    name = 'ScienceSpider'
    allowed_domain = ['science.com.cn']
    start_urls= ['http://science.china.com.cn/']
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    rules = (
       Rule(SgmlLinkExtractor(allow=(r'http://science.china.com.cn/\d{4}-\d{2}/\d+/content_\d+.htm'),restrict_xpaths=('//div[@class="TopNews" or @class="News_left" or @class="AppBox" or @class="Videos_left" or @class="News_right_left" or @class="Technology_left" or @class="Technology_center" or @class="Technology_right"]'),deny_extensions=""),callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = WebArticleItem()
        i['siteName'] = 'science'
        i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
        i['url'] = response.url
        pubtime=sel.xpath('//span[@id="pubtime_baidu"]/text()').re(r'\d{4}-\d{2}-\d{2}')
        i['publishTime'] = len(pubtime)>0 and pubtime[0] or str(datetime.date.today())
        i['addTime'] = datetime.datetime.now()
        author = sel.xpath('//span[@id="author_baidu"]/text()').extract()
        i['author'] = len(author)>0 and author[0].split(u'\uff1a')[1].strip() or ''
        if len(sel.xpath('//span[@id="source_baidu"]/font/text()').extract())>0:
            source = sel.xpath('//span[@id="source_baidu"]/font/text()').extract()
            i['source'] = len(source)>0 and source[0].strip() or ''
        else:
            source = sel.xpath('//span[@id="source_baidu"]/text()').extract()
            i['source'] = len(source)>0 and source[0].split(u'\uff1a')[1].strip() or ''

        i['content'] = (len(sel.xpath('//div[@id="fontzoom"]').extract())) and sel.xpath('//div[@id="fontzoom"]').extract()[0] or ''
        i['keyWords'] = ''
        i['abstract'] = ''
        return i


