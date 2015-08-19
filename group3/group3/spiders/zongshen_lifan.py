# -*- coding: utf-8 -*-

__author__ = 'liufeng'

import datetime
import re
import time

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from group3.items import WebArticleItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

# 写入bbsnew列族

class ZongShenLifanSpider(Spider):
  name = "zongshen_lifan"
  allowed_domains = ["www.lifan.com"]

  start_urls = [
    'http://www.lifan.com/news/list.html'
  ]

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]
    
  def __init__(self,*args, **kwargs):
    super(ZongShenLifanSpider, self).__init__(*args, **kwargs)
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

    news_link_selector_list = xpath.selector('//ul[@class="newslist1"]/li')
    for news_link_selector in news_link_selector_list:
      news_link_xpath = XPath(news_link_selector)
      news_link = news_link_xpath.first('.//a/@href')
      news_link_text = news_link_xpath.first('./i/text()').strip()
      match = re.match('(\d+\.\d+\.\d+)', news_link_text)
      time_str = match.group(1)
      publish_time = datetime.datetime.strptime(time_str, '%Y.%m.%d')

      time.sleep(1)

      yield Request(
        'http://www.lifan.com' + news_link,
        callback=self.parse_news,
        meta={
          'publishTime': publish_time
        }
      )

    next_link = xpath.first('//*[text()="' + u'下一页' + '"]/@href')
    if next_link:
      yield Request('http://www.lifan.com' + next_link, callback=self.parse_list)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="newshowL1"]/.//h1[1]/text()')
    i['url'] = response.url

    i['publishTime'] = response.meta['publishTime']
    if not i['publishTime']:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['source'] = ''
    i['author'] = ''
    i['abstract'] = ''
    i['keyWords'] = ''

    i['content'] = xpath.first('//*[@class="newshowL1"]')

    i['siteName'] = 'www.lifan.com'
    i['newstype'] = u'宗申'
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
