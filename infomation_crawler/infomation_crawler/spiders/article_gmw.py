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

class ArticleGmwSpider(Spider):
  name = "article_gmw"
  allowed_domains = ["tech.gmw.cn"]
  start_urls = [
    'http://tech.gmw.cn/node_5556.htm'
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
    news_url_list = ['http://tech.gmw.cn/' + url for url in xpath.list('//*[@class="channel-newsGroup"]//*[@class="channel-newsTitle"]/a/@href')]
    time_list = xpath.list('//*[@class="channel-newsGroup"]/li/span[@class="channel-newsTime"]/text()')

    continue_next = True

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None

      try:
        publish_time = datetime.datetime.strptime(time_str, '%Y-%m-%d')
      except:
        pass

      if publish_time and publish_time.date() not in self.time_range:
        continue_next = False
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

    if continue_next:
      next_url = xpath.first(u'//*[text()="下一页"]/@href')
      if next_url:
        yield Request('http://tech.gmw.cn/' + next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//h1[@id="articleTitle"]/text()')
    i['url'] = response.url

    source = '\n'.join(xpath.list('//*[@id="source"]//text()'))
    match = re.match(ur'来源：.*?(\S+)', source, re.DOTALL)
    if match:
      i['source'] = match.group(1)
    else:
      i['source'] = ''

    i['author'] = ''
    i['publishTime'] = response.meta['publishTime']
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)
    i['abstract'] = xpath.first('//*[@name="description"]/@content')
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@id="contentMain"]')
    i['siteName'] = 'tech.gmw.cn'
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
