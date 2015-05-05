from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from group2.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class demoSpider(CrawlSpider):
    name = 'demo'
    allowed_domains = ['ccidnet.com']
    start_urls = ['http://news.ccidnet.com/col/1032/1032.html']

    conn = pymongo.Connection('172.20.8.3',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles

    def parse_item(self, response):
        sel = Selector(response)
        i = response.meta['item']

        info = sel.xpath('//div[@class="cont-div2"]/h3/text()').extract()
        info = len(info)>0 and info[0].strip().split('\n\t\t\t\t') or ''
        i['publishTime'] = len(info)>3 and info[0].strip().replace(u'\u53d1\u5e03\u65f6\u95f4\uff1a','').split()[0].replace('.','-') or str(datetime.date.today())
        i['source'] = len(info)>3 and info[2].strip().replace(u'\u6765\u6e90\uff1a','') or ''
        i['author'] = len(info)>3 and info[3].strip().replace(u'\u4f5c\u8005\uff1a','').replace(' ',',') or ''

        content = sel.xpath('//div[@class="temp"]').extract()
        i['content'] = len(content)>0 and content[0] or ''

        i['siteName'] = 'ccidnet'

        i['addTime'] = datetime.datetime.now()

        i['keyWords'] = ''

        return i

    def parse(self, response):
        print "enter ccidnet_parse_item...."
        sel = Selector(response)
        items = []
        newsLists = sel.xpath('//div[@class="cont-left-div-1"]/table/tr/td/table/tr')[0:]
        for news in newsLists:
            i = WebArticleItem()
            i['url'] = 'http://news.ccidnet.com'+news.xpath('td[2]/a/@href').extract()[0]

            title = news.xpath('td[2]/a/text()').extract()
            i['title'] = len(title)>0 and title[0].strip() or ''

            i['abstract'] = ''

            items.append(i)
        for item in items:
            yield Request(item['url'],meta={'item':item},callback=self.parse_item)
