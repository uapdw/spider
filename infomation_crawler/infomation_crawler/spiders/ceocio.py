from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class CeocioSpider(CrawlSpider):
  name = 'ceocio'
  allowed_domains = ['ceocio.com.cn']
  start_urls = ['http://www.ceocio.com.cn/net/cloud/','http://www.ceocio.com.cn/net/moving/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    newsFrom = sel.xpath('//span[@class="news_from"]/text()').extract()
    info = len(newsFrom)>0 and newsFrom[0].split() or ''
    i['source'] = len(info)>2 and info[1].split(u'\uff1a')[1].strip() or ''
    i['author'] = len(info)>2 and info[2].split(u'\uff1a')[1].strip() or ''

    content = sel.xpath('//li[@class="news_body"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['keyWords'] = ''
    i['siteName'] = 'ceocio'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter ceocio_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//li[@class="Title_list"]/dl/dd')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://www.ceocio.com.cn'+news.xpath('a/@href').extract()[0]
      
      title = news.xpath('a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      i['abstract'] = ''

      pubTime = news.xpath('span/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].strip() or str(datetime.date.today())
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
