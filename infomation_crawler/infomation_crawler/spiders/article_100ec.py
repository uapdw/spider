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

class Article100ecSpider(Spider):
  name = "article_100ec"
  allowed_domains = ["100ec.cn"]
  start_urls = [
    'http://www.100ec.cn/search.cgi?p=1&f=search&terms=%B5%E7%C9%CC%D6%D0%D0%C4%C8%D5%B2%A5',
    'http://www.100ec.cn/list--21--1.html',
    'http://www.100ec.cn/list--22--1.html',
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
    # 搜索走下一页逻辑，列表取前10页
    yield Request('http://www.100ec.cn/search.cgi?p=1&f=search&terms=%B5%E7%C9%CC%D6%D0%D0%C4%C8%D5%B2%A5', callback=self.parse_list)

    for start_url_pattern in ['http://www.100ec.cn/list--21--%s.html', 'http://www.100ec.cn/list--22--%s.html']:
      for i in range(1, 10):
        yield Request(start_url_pattern % i, callback=self.parse_list)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = ['http://www.100ec.cn' + news_url for news_url in xpath.list('//*[@class="cnews"]/ul/li/a/@href')]
    time_list = xpath.list('//*[@class="cnews"]/ul/li/span/text()')

    continue_next = True

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None

      match = re.match(r'\((\d+)-(\d+)-(\d+)\)', time_str)
      if match:
        publish_time = datetime.datetime(int(str(datetime.datetime.now().year)[:2] + match.group(1)), int(match.group(2)), int(match.group(3)))

      if not publish_time:
        match = re.match(r'\((\d+)-(\d+)\)', time_str)
        if match:
          publish_time = datetime.datetime(datetime.datetime.now().year, int(match.group(1)), int(match.group(2)))

      if publish_time and publish_time.date() not in self.time_range:
        continue_next = False
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

    if continue_next:
      if 'http://www.100ec.cn/search.cgi' in response.url: # 搜索走下一页
        next_url = xpath.first(u'//a[text()="下一页"]/@href')
        if next_url:
          yield Request('http://www.100ec.cn' + next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="newsview"]/h2/text()')
    i['url'] = response.url

    i['source'] = ''
    i['author'] = ''
    i['publishTime'] = response.meta['publishTime']

    top_info = '\n'.join(xpath.list('//*[@class="public f_hong"]/text()'))
    
    match = re.match(ur'.*?(\S+)\s+(\d+)年(\d+)月(\d+)日(\d+):(\d+)', top_info, re.DOTALL)
    if match:
      i['source'] = match.group(1)
      print match.group(2)
      publish_time = datetime.datetime(int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6)))
      if publish_time:
        i['publishTime'] = publish_time
        
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)

    i['abstract'] = xpath.first('//meta[@name="description"]/@content')
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@class="newsview"]')
    i['siteName'] = 'www.100ec.cn'
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
