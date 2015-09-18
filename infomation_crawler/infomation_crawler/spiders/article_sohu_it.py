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

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
  
class ArticleSohuIT(Spider):
  name = "article_sohu_it"
  allowed_domains = ["mt.sohu.com"]
  start_urls = [
    'http://mt.sohu.com/it/index.shtml'
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
    news_url_list = [url for url in xpath.list('//h3/span[@class="content-title"]/a/@href')]
    time_list = xpath.list('//p[@class="publish-footer"]/span[@class="time"]/text()')

    for url, time_str in zip(news_url_list, time_list):
      publish_time = None
      try:
        print time_str
        publish_time = datetime.datetime.strptime(time_str,'%Y年%m月%d日%H:%M')
      except:
        pass

      if publish_time and publish_time.date() not in self.time_range:
        continue

      yield Request(url, callback=self.parse_news, meta={'publishTime': publish_time})

    
    script_str = xpath.first('//div[@class="pages"]//script/text()').replace('\t','').split('\n')
    maxPage = script_str[2].replace(';','').replace('var maxPage = ','').strip()
    curPage = script_str[3].replace(';','').replace('var curPage = ','').strip()
    next_url = 'http://mt.sohu.com/it/index_' + str(int(maxPage) - int(curPage)) + '.shtml'

    yield Request(next_url, callback=self.parse_list)


  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    print response.meta['publishTime']
    print '='*50

    i['title'] = xpath.first('//h1/text()')
    i['url'] = response.url
    i['source'] = xpath.first('//*[@id="container"]/div[1]/div[1]/div[1]/div/span[1]/a/text()')
    i['author'] = ''
    i['publishTime'] = str(response.meta['publishTime'].date()) if response.meta['publishTime'] else str(self.yesterday)
    i['abstract'] = ''
    i['keyWords'] = ' '.join([w for w in xpath.list('//div[@class="news-writer clear"]/span[@class="tag"]/a/text()')])
    i['content'] = xpath.first('//div[@itemprop="articleBody"]')
    i['siteName'] = 'mt.sohu.com'
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
