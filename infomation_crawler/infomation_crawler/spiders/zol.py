from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ZolSpider(CrawlSpider):
  name = 'zol'
  allowed_domains = ['cio.zol.com.cn', 'cloud.zol.com.cn']
  start_urls = ['http://cio.zol.com.cn/', 'http://cloud.zol.com.cn/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/\d+/\d+\.html'), callback='parse_item', follow=True),
  )

  def __init__(self,**kw):
    super(ZolSpider,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)


  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    print "enter Zol_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'zol'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@id="article-content"]').extract())) and sel.xpath('//div[@id="article-content"]').extract()[0] or ''
    i['publishTime'] = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0]
    i['keyWords'] = ''
    i['author'] = ''
    i['abstract'] = ''
    i['source'] = ''
    return i

