# -*- coding: utf-8 -*-

__author__ = 'liufeng'

import datetime
import re

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import FormRequest
from group3.items import WebArticleItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

# 写入bbsnew列族

class ZongShenCCSpider(Spider):
  name = "zongshen_zongshencc"
  allowed_domains = ["www.zongshen.cc"]

  start_urls = [
    'http://www.zongshen.cc/news/default.aspx',
  ]

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]

  def __init__(self,*args, **kwargs):
    super(ZongShenCCSpider, self).__init__(*args, **kwargs)
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
      yield Request(start_url, meta={'cookiejar': 1})

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))

    news_link_selector_list = xpath.selector('//ul[@class="listnews"]/li')
    for news_link_selector in news_link_selector_list:
      news_link_xpath = XPath(news_link_selector)
      news_link = news_link_xpath.first('./a/@href')
      time_str = news_link_xpath.first('./*[@class="time"]/text()').strip()
      publish_time = datetime.datetime.strptime(time_str, '%Y-%m-%d')

      if self.increment and publish_time not in self.time_range:
        continue

      yield Request(
        'http://www.zongshen.cc/news/' + news_link,
        callback=self.parse_news,
        meta={
          'publishTime': publish_time
        }
      )

    next_link = xpath.first('//*[@class="prenext" and text()="' + u'下一页' + '"]/@href')
    if next_link:
      match = re.match('javascript:__doPostBack\(\'AspNetPager1\',\'(\d+)\'\)', next_link)
      page = match.group(1)
      print page

      __EVENTVALIDATION = xpath.first('//input[@name="__EVENTVALIDATION"]/@value')
      __VIEWSTATE = xpath.first('//input[@name="__VIEWSTATE"]/@value')

      yield FormRequest('http://www.zongshen.cc/news/default.aspx', formdata={'__EVENTTARGET': 'AspNetPager1', '__EVENTARGUMENT': page, '__VIEWSTATE': __VIEWSTATE, '__EVENTVALIDATION': __EVENTVALIDATION}, callback=self.parse_list, dont_filter=True)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="fl news"]/.//*[@ class="title"]/text()')
    i['url'] = response.url

    i['publishTime'] = response.meta['publishTime']
    if not i['publishTime']:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['source'] = ''
    i['author'] = ''
    i['abstract'] = ''
    i['keyWords'] = ''

    i['content'] = xpath.first('//*[@class="fl news"]/.//*[@class="content"]')

    i['siteName'] = 'www.zongshen.cc'
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
