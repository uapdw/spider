# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
import re
import datetime
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class NewsCheaaSpider(Spider):
  name = "newscheaa"
  allowed_domains = ["cheaa.com"]
  start_urls = [
    'http://news.cheaa.com/hangye.shtml'
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
    news_url_list = xpath.list('//*[@id="main-list"]/div[contains(@class,"ListPageBox")]/.//a/@href')
    time_list = xpath.list('//*[@id="main-list"]/div[contains(@class,"ListPageBox")]/.//span[@class="liright"]/text()')
    for news_url, time in zip(news_url_list, time_list):
      publish_time = None
      try:
        match = re.match(u'(\d+)年(\d+)月(\d+)日', time)
        time = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
        publish_time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
      except:
        pass

      if publish_time in self.time_range:
        yield Request(news_url, callback=self.parse_news)

    last_publish_time = None
    try:
      match = re.match(u'(\d+)年(\d+)月(\d+)日', time_list[len(time_list)-1])
      last_time = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
      last_publish_time = datetime.datetime.strptime(last_time, '%Y-%m-%d').date()
    except:
      pass

    if last_publish_time in self.time_range:
      next_url = xpath.first('//a[@class="next"]/@href')
      if next_url:
        yield Request(next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()
    i['title'] = xpath.first('//*[@id="NewsTitle"]/h1/text()')
    i['url'] = response.url

    i['publishTime'] = None
    
    news_info = xpath.first('//*[@id="NewsInfo"]/text()')
    match = re.match(u'(\d\d\d\d-\d\d-\d\d \d\d:\d\d).*:\s+(\S+)\s+(\S+)', news_info, re.UNICODE)
    if match:
      time_str = match.group(1)
      i['source'] = match.group(2)
      i['author'] = match.group(3)
      try:
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass
    else:
      match = re.match(u'(\d\d\d\d-\d\d-\d\d \d\d:\d\d).*:\s+(\S+)', news_info, re.UNICODE)
      if match:
        time_str = match.group(1)
        try:
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        except:
          pass
        i['source'] = match.group(2)
        i['author'] = ''
      else:
        i['source'] = ''
        i['author'] = ''

    if not i['publishTime']:
      i['publishTime'] = datetime.datetime(1970,1,1)

    
    i['abstract'] = xpath.first('//*[@name="description"]/@content')
    i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')
    i['siteName'] = u'中国家电信息网'
    i['newstype'] = u'家电'
    i['content'] = xpath.first('//*[@id="ctrlfscont"]')
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
