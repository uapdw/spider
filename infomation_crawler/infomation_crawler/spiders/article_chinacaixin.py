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

class ArticleChinacaixinSpider(Spider):
  name = "article_chinacaixin"
  allowed_domains = ["www.chinacaixin.com"]
  start_urls = [
    'http://www.chinacaixin.com/NewsList.asp?lm=568',
    'http://www.chinacaixin.com/NewsList.asp?lm=569',
    'http://www.chinacaixin.com/NewsList.asp?lm=617',
    'http://www.chinacaixin.com/NewsList.asp?lm=620',
    'http://www.chinacaixin.com/NewsList.asp?lm=624',
    'http://www.chinacaixin.com/NewsList.asp?lm=625',
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
    news_url_list = ['http://www.chinacaixin.com/' + url for url in xpath.list('//a[starts-with(@href, "NewsView.asp")]/@href')]

    for news_url in news_url_list:
      yield Request(news_url, callback=self.parse_news)

    continue_next = True

    next_url = 'http://www.chinacaixin.com/NewsList.asp' + xpath.first('//*[@class="page-next"]/@href')
    match = re.match(r'.*?page=(\d+)', next_url)
    if match:
      next_page = int(match.group(1))
      if next_page > 5:
        continue_next = False

    if continue_next:
      yield Request(next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="font_20"]/text()')
    i['url'] = response.url
    i['source'] = ''
    i['author'] = ''

    publish_time = None
    match = re.match(r'.*?(\d{4}-\d+-\d+ \d+:\d+:\d+)', response.body, re.DOTALL)
    if match:
      try:
        publish_time = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
      except:
        pass

    if not publish_time or publish_time.date() not in self.time_range:
      return

    i['publishTime'] = publish_time
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)
    i['abstract'] = '\n'.join(xpath.list('//*[@class="describe"]/text()')).strip()
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@id="content"]')
    i['siteName'] = 'www.chinacaixin.com'
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
