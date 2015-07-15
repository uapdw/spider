from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebBBSItem
import datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ItpubSpider(CrawlSpider):
  name = 'itpub'
  allowed_domains = ['itpub.net']
  start_urls = ['http://www.itpub.net/forum.php']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebBlogs = infoDB.web_blogs

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/forum-\d-\d-\.html')),
    Rule(SgmlLinkExtractor(allow=r'/thread-\d-\d-\d\.html'), callback='parse_item'),
  )

  def __init__(self,**kw):
    super(ItpubSpider,self).__init__(**kw)
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
    i = WebBBSItem()
    i['title'] = sel.xpath('//a[@id="thread_subject"]/text()').extract()[0]
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = sel.xpath('//div[@id="blog_content"]').extract()[0]
    i['siteName'] = 'itpub'
    i['author'] = sel.xpath('//div[@id="blog_owner_name"]/text()').extract()[0]
    return i

