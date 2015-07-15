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
class CiotimesSpider(CrawlSpider):
  name = 'ciotimes'
  allowed_domains = ['ciotimes.com']
  start_urls = ['http://www.ciotimes.com/cio_chanel/rwsc/','http://www.ciotimes.com/100j/jbft/']

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

    author = sel.xpath('//div[@class="f12"]/text()').extract()
    i['author'] = len(author)>0 and author[0].strip().split()[0].split(u'\uff1a')[1] or ''
    i['source'] = ''

    content = sel.xpath('//div[@class="n1_1_5 f14 close kfc"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'ciotimes'

    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@class="n1_1_5m f12 close"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter ciotimes_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="l1_1"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://www.ciotimes.com/'+news.xpath('div[@class="l1_1_1"]/div[1]/a/@href').extract()[0]
      
      title = news.xpath('div[@class="l1_1_1"]/div[1]/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('div[@class="l1_1_2 f12"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''

      pubTime = news.xpath('div[@class="l1_1_1"]/div[2]/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].strip() or str(datetime.date.today())
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
