# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from group3.items import WebBBSItem
from urlparse import urlparse
import datetime
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class BaisejiadianTiebaSpider(CrawlSpider):
  name = "baisejiadiantieba"

  allowed_domains = ["tieba.baidu.com"]
  start_urls = [
    'http://tieba.baidu.com/f?kw=%E7%99%BD%E8%89%B2%E5%AE%B6%E7%94%B5&ie=utf-8&pn=0'
  ]

  rules = (
    Rule(LinkExtractor(allow=('f?kw=%E7%99%BD%E8%89%B2%E5%AE%B6%E7%94%B5&ie=utf-8&pn=\d+'), restrict_xpaths=('//*[@class="next"]'))),
    Rule(LinkExtractor(allow=('/p/\d+')), callback='parse_thread'),
  )
    
  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  def __init__(self,**kw):
    super(BaisejiadianTiebaSpider,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)


  def __del__(self):
    self.transport.close()

  def parse_thread(self, response):

    xpath = XPath(Selector(response))
    i = WebBBSItem()

    i['title'] = xpath.first('//*[@class="core_title_txt  "]/@title')
    i['author'] = xpath.first('//*[@class="p_author"]/*[@class="d_name"]/a/text()')
    i['url'] = response.url
    i['source'] = ''

    i['publishTime'] = None

    try:
      time_str = xpath.first('//*[@class="core_reply_tail "]/*[@class="p_tail"]/li[2]/span/text()')
      i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    except:
      pass

    if i['publishTime']:
      if i['publishTime'].date() not in self.time_range:
        return
    else:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['abstract'] = ''
    i['keyWords'] = ''
    i['content'] = xpath.first('//*[starts-with(@id, "post_content_")]')
    i['siteName'] = 'tieba.baidu.com'
    i['addTime'] = datetime.datetime.now()

    return i

  def domain_url(self, url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain

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
