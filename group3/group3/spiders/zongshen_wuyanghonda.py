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

class ZongShenWuyanghondaSpider(Spider):
  name = "zongshen_wuyanghonda"
  allowed_domains = ["www.wuyang-honda.com"]

  start_urls = [
    'http://www.wuyang-honda.com/news/company_news.jsp?catid=21'
  ]

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]

  def __init__(self,*args, **kwargs):
    super(ZongShenWuyanghondaSpider, self).__init__(*args, **kwargs)
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

    news_link_selector_list = xpath.selector('//*[@class="ar_li"]/.//tr')
    for news_link_selector in news_link_selector_list:
      news_link_xpath = XPath(news_link_selector)
      news_link = news_link_xpath.first('./td[2]/a/@href')
      news_link_text = news_link_xpath.first('./td[3]/text()').strip()
      publish_time = datetime.datetime.strptime(news_link_text, '%Y-%m-%d')

      if self.increment and publish_time not in self.time_range:
        continue

      yield Request(
        'http://www.wuyang-honda.com' + news_link[2:],
        callback=self.parse_news,
        meta={
          'publishTime': publish_time
        }
      )

    next_link = xpath.first('//*[contains(@src, "new_page_55.gif")]/../@href')
    if next_link:
      match = re.match('javascript:gotopage\((\d+)\);', next_link)
      page = match.group(1)
      yield FormRequest('http://www.wuyang-honda.com/news/company_news.jsp?catid=21', formdata={'pageno': page, 'catid': '21'}, callback=self.parse_list, dont_filter=True)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="archive_title"]/text()')
    i['url'] = response.url

    i['publishTime'] = response.meta['publishTime']
    if not i['publishTime']:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['source'] = ''
    i['author'] = ''
    i['abstract'] = ''
    i['keyWords'] = ''

    i['content'] = xpath.first('//*[@class="archive_content"]')

    i['siteName'] = 'www.wuyang-honda.com'
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
