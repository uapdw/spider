# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from infomation_crawler.items import WebArticleItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ArticleKn58Spider(CrawlSpider):
  name = "article_kn58"
  allowed_domains = ["kn58.com"]
  start_urls = [
    'http://www.kn58.com/tech/'
  ]

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))

  link_pattern = 'www.kn58.com/tech/\S*?/detail_%Y_%m%d/\d+\.html'

  rules = (
    # Rule(LinkExtractor(allow=('www.kn58.com/tech/\S*?/detail_\d+_\d+/\d+.html')), callback='parse_news'),
    Rule(LinkExtractor(allow=(today.strftime(link_pattern))), callback='parse_news'),
    Rule(LinkExtractor(allow=(yesterday.strftime(link_pattern))), callback='parse_news'),
    Rule(LinkExtractor(allow=('www.kn58.com/tech/.*'), deny=('www.kn58.com/tech/\S*?/detail_\d+_\d+/\d+\.html', 'www.kn58.com/tech/\S*?/list_\d{2,}\.html'))), # detail页不follow， list页取前9页
  )
    
  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
  def __init__(self,*args, **kwargs):
    super(ArticleKn58Spider, self).__init__(*args, **kwargs)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="title"]/h1/text()')
    i['url'] = response.url

    i['source'] = ''
    i['publishTime'] = None

    titlefu = xpath.first('//*[@class="titiefu"]/text()')
    titlefu = titlefu.replace(u'\xa0', u' ')
    match = re.match(ur'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*来源：(\S+)\s*', titlefu)
    if match:
      i['source'] = match.group(2)
      try:
        i['publishTime'] = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
      except:
        pass
    
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)

    i['author'] = ''
    i['abstract'] = '\n'.join(xpath.list('//*[@id="chjof"]/text()'))
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@class="daaovbqslk"]')
    i['siteName'] = 'www.kn58.com'
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
