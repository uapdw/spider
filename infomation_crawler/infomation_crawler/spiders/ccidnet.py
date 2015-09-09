# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'zhangxin'

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
from scrapy.exceptions import DropItem

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
class CcidnetSpider(CrawlSpider):
  name = 'ccidnet'
  allowed_domains = ['ccidnet.com']
  start_urls = [
    'http://www.ccidnet.com/news/',
    'http://www.ccidnet.com/internet/',
    'http://www.ccidnet.com/product/',
    'http://www.ccidnet.com/security/',
    'http://www.ccidnet.com/information/',
    'http://www.ccidnet.com/smartindustry/',
    'http://www.ccidnet.com/smartcity/',
    'http://www.ccidnet.com/smartlife/',
    
  ]

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  rules = (
    Rule(SgmlLinkExtractor(allow=r'www\.ccidnet\.com/\d{4}/\d{4}/\d+.shtml'), callback='parse_item'),
  )

  def __init__(self,**kw):
    super(CcidnetSpider,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    authorStrList = xpath.first('//div[@class="nr_cont1 F_Left"]/div[@class="tittle_j"]/text()').split()
    publishTime = authorStrList[0].split('：')[1]
    pubTime = datetime.datetime.strptime(publishTime,'%Y-%m-%d')

    if pubTime and pubTime.date() not in self.time_range:
      raise DropItem('publishTime is out of the time range: %s' % publishTime)

    i['title'] = xpath.first('//div[@class="nr_cont1 F_Left"]/h2/text()')
    i['url'] = response.url
    i['source'] = authorStrList[2].split('：')[1]
    i['author'] = authorStrList[3].split('：')[1]
    i['publishTime'] = publishTime
    i['abstract'] = xpath.first('//div[@class="nr_cont1 F_Left"]/div[@class="p_jd"]/text()')
    i['keyWords'] = ' '.join([w for w in xpath.list('//div[@class="cont2_tittle"]/div[@class="gjc F_Left"]/a/text()')])
    i['content'] = xpath.first('//div[@class="main_content"]')
    i['siteName'] = 'www.ccidnet.com'
    i['addTime'] = datetime.datetime.now()

    return i


class XPath():

  _selecter = None

  def __init__(self, selector):
    self._selecter = selector

  def selector(self, xpath = None):
    if xpath:
      return self._selecter.xpath(xpath)
    else:
      return self._selecter

  def list(self, path):
    return [s.strip() for s in self._selecter.xpath(path).extract() if s.strip()]

  def first(self, path):
    l = self.list(path)
    if l:
      return l[0].strip()
    else:
      return ''
