# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
from urlparse import urlparse
import re
import datetime
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class Hea163Spider(Spider):
  name = "hea163"
  allowed_domains = ["163.com"]
  start_urls = [
    'http://hea.163.com/'
  ]

  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def start_requests(self):
    for start_url in self.start_urls:
      yield Request(start_url)

  def parse(self, response):
    yield Request('http://hea.163.com/special/jiadian_data/', callback=self.parse_list)

    for page in range(2, 6):
      yield Request('http://hea.163.com/special/jiadian_data_0' + str(page) + '/', callback=self.parse_list)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//li/div/h3/a/@href')

    for news_url in news_url_list:
      yield Request(news_url, callback=self.parse_news)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@id="h1title"]/text()')

    i['url'] = response.url

    i['source'] = xpath.first('//*[contains(@class, "ep-time-soure")]/a/text()')
    i['author'] = xpath.first('//*[@class="ep-editor"]/text()') # 责任编辑
    
    i['publishTime'] = None
    
    try:
      time_str = xpath.first('//*[contains(@class, "ep-time-soure")]/text()[1]')
      match = re.match(u'\s*(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)\s*来源', time_str, re.UNICODE)
      if match:
        time_str = match.group(1) + '-' + match.group(2) + '-' + match.group(3) + ' ' + match.group(4) + ':' + match.group(5) + ':' + match.group(6)
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    except:
      pass

    if not i['publishTime']:
      i['publishTime'] = datetime.datetime.now()

    i['abstract'] = xpath.first('//*[@id="endText"]/p')
    i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@id="endText"]')

    i['siteName'] = u'艾肯家电网'
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
