from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class itSpider(CrawlSpider):
  name = '199it'
  allowed_domains = ['199it.com']
  start_urls = ['http://www.199it.com/archives/tag/%E5%A4%A7%E6%95%B0%E6%8D%AE','http://www.199it.com/archives/category/dataindustry/data-mining']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    pubTime = sel.xpath('//div[@id="meta-hidden"]/a[@class="post-time"]/time/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].replace(u'\u5e74','-').replace(u'\u6708','-').replace(u'\u65e5','').strip() or str(datetime.date.today())

    author = sel.xpath('//div[@id="meta-hidden"]/span[@class="author vcard"]/a/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''

    content = sel.xpath('//div[@class="entry-content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = '199it'

    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@id="meta-hidden"]/a[@rel="tag"]/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter 199it_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="entry-list-right"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h2/a/@href').extract()[0]
      
      title = news.xpath('h2/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('p/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
