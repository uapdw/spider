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

class TechqqSpider(CrawlSpider):
  name = 'techqq'
  allowed_domains = ['qq.com']
  start_urls = ['http://tech.qq.com/hlwxw.htm']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
 
  def __init__(self,**kw):
    super(TechqqSpider,self).__init__(**kw)
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

    source = sel.xpath('//span[@class="infoCol"]/span[@class="where"]/text()').extract()
    i['source'] = len(source)>0 and source[0].strip() or ''
    author = sel.xpath('//span[@class="infoCol"]/span[@class="auth"]/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''
    pubTime = sel.xpath('//span[@class="pubTime"]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split(u'\u65e5')[0].strip().replace(u'\u5e74','-').replace(u'\u6708','-') or str(datetime.date.today())

    content = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'tech.qq'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter techqq_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="Q-tpList"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h3/a/@href').extract()[0]
      
      title = news.xpath('h3/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('p[@class="l23"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''
       
      keyWordList = news.xpath('div[@class="newsinfo cf"]/div/span[2]/em/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords
    
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
