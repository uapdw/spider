# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'zhangxin'

import re
import datetime
import time

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from infomation_crawler.items import WebArticleItem
from scrapy.exceptions import DropItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
  
class ArticleQQFinance(Spider):
  name = "article_qq_finance"
  allowed_domains = ["qq.com"]
  # start_urls = [
  #   'http://finance.qq.com/gsbd.htm',
  #   'http://finance.qq.com/hgjj.htm'
  # ]

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
    for start_url_pattern in ['http://finance.qq.com/c/hgjjllist_%s.htm?0.34141235868020936', 'http://finance.qq.com/c/gsbdlist_%s.htm?0.128716753766128']:
      for i in range(1, 5):
        yield Request(start_url_pattern % i, callback=self.parse_list)


  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = ['http://finance.qq.com' + url for url in xpath.list('//div[@class="Q-tpWrap"]/em/a/@href')]
    time_list = xpath.list('//p[@class="time l22"]/text()')

    for url, time_str in zip(news_url_list, time_list):
      # print url, time_str

      # publish_time = None
      # try:
      #   publish_time = datetime.datetime.strptime(time_str,'%m月%d日 %H：%M')
      # except:
      #   pass

      # print publish_time

      # if publish_time and publish_time.date() not in self.time_range:
      #   continue

      yield Request(url, callback=self.parse_news)


  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    publishTime = xpath.first('//span[@class="pubTime article-time"]/text()')
    pubTime = datetime.datetime.strptime(publishTime, '%Y-%m-%d %H:%M')
    if pubTime and pubTime.date() not in self.time_range:
      raise DropItem('publishTime is out of the time range: %s' % publishTime)

    i['title'] = xpath.first('//h1/text()')
    i['url'] = response.url
    i['source'] = xpath.first('//span[@class="where color-a-1"]/text()')
    i['author'] = ''
    i['publishTime'] = pubTime.strftime('%Y-%m-%d')
    i['abstract'] = ''
    i['keyWords'] = ''
    i['content'] = xpath.first('//*[@id="Cnt-Main-Article-QQ"]')
    i['siteName'] = 'finance.qq.com'
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
