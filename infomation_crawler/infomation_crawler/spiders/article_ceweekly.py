# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from infomation_crawler.items import WebArticleItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ArticleCeweeklySpider(Spider):
  name = "article_ceweekly"
  allowed_domains = ["www.ceweekly.cn"]
  start_urls = [
    'http://www.ceweekly.cn/company/',
    'http://www.ceweekly.cn/economic/it/'
  ]

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
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
    news_url_list = xpath.list('//*[@class="column-main"]//*[@class="item"]/a/@href')
    time_list = xpath.list('//*[@class="column-main"]//*[@class="item"]/span/text()')

    continue_next = True

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None

      match = re.match(ur'(\d{4})年(\d+)月(\d+)日\s*(\d+):(\d+)', time_str)
      if match:
        publish_time = datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)))

      if publish_time and publish_time.date() not in self.time_range:
        continue_next = False
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

    if continue_next:
      next_url = xpath.first('//*[@class="next"]/@href')
      if next_url:
        yield Request(next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="article-title"]/text()')
    i['url'] = response.url

    source = '\n'.join(xpath.list('//*[@class="source"]//text()'))
    match = re.match(ur'来源:.*?(\S+)', source, re.DOTALL)
    if match:
      i['source'] = match.group(1)
    else:
      i['source'] = ''

    i['author'] = ''
    i['publishTime'] = response.meta['publishTime']
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)
    i['abstract'] = '\n'.join(xpath.list('//*[@class="describe"]/text()')).strip()
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[contains(@class, "article-content")]')
    i['siteName'] = 'www.ceweekly.cn'
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
