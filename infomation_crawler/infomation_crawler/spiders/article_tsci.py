# -*- coding: utf-8 -*-


__author__ = 'liufeng'

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

class ArticleTsciSpider(Spider):
  name = "article_tsci"
  allowed_domains = ["data.tsci.com.cn"]
  start_urls = [
    'http://data.tsci.com.cn/News/Default.aspx?Kind=c00011',
    'http://data.tsci.com.cn/News/Default.aspx?Kind=c00009',
    'http://data.tsci.com.cn/News/Default.aspx?Kind=konson',
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

  def start_requests(self):
    # 取前10页
    for start_url in self.start_urls:
      for i in range(0, 9):
        yield Request('%s&P=%s' % (start_url, i))

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = [news_url if 'http://data.tsci.com.cn/' in news_url else 'http://data.tsci.com.cn/' + news_url for news_url in xpath.list('//*[@class="News_list"]/li/a/@href')]
    time_list = xpath.list('//*[@class="News_list"]/li/em/text()')

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None
      try:
        publish_time = datetime.datetime.strptime(time_str, '%Y/%m/%d %H:%M')
      except:
        pass

      if publish_time and publish_time.date() not in self.time_range:
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="NewsTit"]/text()')
    i['url'] = response.url
    i['source'] = ''
    i['author'] = ''
    i['publishTime'] = str(response.meta['publishTime'].date()) if response.meta['publishTime'] else str(self.yesterday)
    i['abstract'] = xpath.first('//meta[@name="description"]/@content')
    i['keyWords'] = xpath.first('//meta[@name="keyword"]/@content')
    i['content'] = xpath.first('//*[@class="NewsCon"]')
    i['siteName'] = 'data.tsci.com.cn'
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
