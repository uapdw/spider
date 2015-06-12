# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy.http import Request
import re
class CctimeSpider(CrawlSpider):
    name = 'cctime'
    allowed_domain = ['cctime.com']
    urls=[]
    for i in range(1,16):
        url = 'http://www.cctime.com/scroll/default.asp?kpage='+ str(i)
        urls.append(url)
    start_urls= urls
    conn = pymongo.Connection('172.20.8.3',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    #rules = [
    #   Rule(SgmlLinkExtractor(allow=(r'http://www.cctime.com/scroll/default.asp\?kpage=\d+'))),
    #   Rule(SgmlLinkExtractor(allow=(r'http://www.cctime.com/html/\d{4}-\d{2}-\d{2}/\d+.htm'),restrict_xpaths=('//td[@id="zList"]')),callback='parse_item'),
    #]

    def parse_item(self, response):
        re_h=re.compile(r'(\xa0)+')
        sel = Selector(response)
        i = response.meta['item']
        i['siteName'] = 'cctime'
        title = sel.xpath('/html/body/table[5]/tr/td[1]/table[1]/tr[1]/td/table/tr[1]/td/text()').extract()
        if (len(title)>1):
            title = sel.xpath('/html/body/table[5]/tr/td[3]/table[1]/tr[2]/td/text()').extract()
        i['title'] = len(title)>0 and title[0].replace(u'\xa0','').strip() or ''
        pubtime = sel.xpath('/html/body/table[5]/tr/td[1]/table[1]/tr[1]/td/table/tr[4]/td/table/tr/td[1]/text()').extract()
        if (len(pubtime)<1):
            pubtime = sel.xpath('/html/body/table[5]/tr/td[3]/table[2]/tr/td/text()').extract()
            i['publishTime'] = len(pubtime)>0 and pubtime[0].split(' ')[0].replace(u'\u5e74','-').replace(u'\u6708','-').replace(u'\u65e5','') or str(datetime.date.today())
            i['source'] = len(pubtime)>0 and pubtime[0].split(' ')[2] or ''
            i['author'] = len(sel.xpath('/html/body/table[5]/tr/td[3]/table[2]/tr/td/a/text()').extract())>0 and sel.xpath('/html/body/table[5]/tr/td[3]/table[2]/tr/td/a/text()').extract()[0] or ''
        else:
            re_h_temp =  re_h.sub('@',pubtime[0]).split('@')
            i['publishTime'] = len(re_h_temp)>0 and re_h_temp[0].split(' ')[0].replace(u'\u5e74','-').replace(u'\u6708','-').replace(u'\u65e5','') or str(datetime.date.today())
            #author = sel.xpath('//span[@id="author_baidu"]/text()').extract()
            i['author'] = len(re_h_temp[2])>0 and re_h_temp[2] or ''
            i['source'] = len(re_h_temp)>0 and re_h_temp[1] or ''
        i['addTime'] = datetime.datetime.now()
        content = sel.xpath('//div[@class="art_content"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['abstract'] = ''
        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        re_g=re.compile(r'http://www.cctime.com/html/\d{4}-\d{2}-\d{2}/\d+.htm')
        url=sel.xpath('//div[@class="kcs_list"]')[0:]
        for newsurl in url:
            i = WebArticleItem()
            url_temp = newsurl.xpath('span[2]/a/@href').extract()[0]
            if re_g.match(url_temp):
                i['url'] = url_temp
                i['keyWords'] = len(newsurl.xpath('span[3]/a/text()').extract())>0 and newsurl.xpath('span[3]/a/text()').extract()[0] or ''
                items.append(i)
        for item in items:
            yield Request(item['url'],meta={'item':item},callback=self.parse_item)








