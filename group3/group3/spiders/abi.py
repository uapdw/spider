# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy import Spider
from group3.items import WebArticleItem
from urlparse import urlparse
import datetime
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class AbiSpider(Spider):
  name = "abi"
  allowed_domains = ["abi.com.cn"]
  start_urls = [
    'http://www.abi.com.cn/news/news-more.asp?lb=2'
  ]
    
  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//*[@id="artlist"]/.//li/.//a/@href')
    time_list = xpath.list('//*[@id="artlist"]/.//li/.//*[@class="times"]/text()')

    domain_url = self.domain_url(response.url)

    for news_url, time in zip(news_url_list, time_list):
      publish_time = None
      try:
        publish_time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
      except:
        pass

      if publish_time in self.time_range:
        yield Request(news_url, callback=self.parse_news)

    last_publish_time = None
    try:
      last_publish_time = datetime.datetime.strptime(time_list[len(time_list)-1], '%Y-%m-%d').date()
    except:
      pass

    if last_publish_time in self.time_range:
      next_url = xpath.first('//a[@class="nxt"]/@href')
      if next_url:
        yield Request(domain_url + '/news/news-more.asp' + next_url, callback=self.parse_list)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="biaoti"]/text()')
    if not i['title']: # 图片新闻
      return

    i['url'] = response.url

    i['source'] = xpath.first('//*[@class="bz1"]/span[2]/text()')
    i['author'] = ''
    
    try:
      time_str = xpath.first('//*[@class="bz1"]/span[1]/text()')
      i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d')
    except:
      i['publishTime'] = datetime.datetime(1970,1,1)

    # 取第一个非空行
    p_list = xpath.list('//*[@id="content"]/p/text()')
    for p in p_list:
      i['abstract'] = p.strip()
      if i['abstract']:
        break

    i['keyWords'] = xpath.first('//*[@name="Keywords"]/@content')
    i['content'] = xpath.first('//*[@id="content"]')

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
