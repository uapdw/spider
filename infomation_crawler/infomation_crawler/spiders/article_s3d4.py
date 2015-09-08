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
  
class ArticleS3d4Spider(Spider):
  name = "article_s3d4"
  allowed_domains = ["s3d4.cn"]
  start_urls = [
    'http://www.s3d4.cn/home/newslist/3_1'
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
    news_url_list = ['http://www.s3d4.cn/' + url for url in xpath.list('//*[@id="left_box"]/*[@class="listbox"]/a/@href')]
    time_list = xpath.list('//*[@id="left_box"]/*[@class="listbox"]/span/text()')

    continue_next = True

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None
      try:
        publish_time = datetime.datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')
      except:
        pass

      if publish_time and publish_time.date() not in self.time_range:
        continue_next = False
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

    if continue_next:
      try:
        current_page = int(re.match(r'.*?/home/\S+?/3_(\d+)', response.url).group(1))
        last_page = int(re.match(r'.*?/home/\S+?/3_(\d+)', xpath.first(u'//a[text()="末页"]/@href')).group(1))
        if last_page != current_page:
          time.sleep(5)
          yield Request('http://www.s3d4.cn/home/newslist/3_%s' % (current_page+1), callback=self.parse_list)
      except:
        pass

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@id="left_box"]//h1/text()')
    i['url'] = response.url
    i['source'] = ''
    i['author'] = ''
    i['publishTime'] = str(response.meta['publishTime'].date()) if response.meta['publishTime'] else str(self.yesterday)
    i['abstract'] = '\n'.join(xpath.list('//*[@class="toptext"]//text()'))
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@class="articlecontent"]')
    i['siteName'] = 'www.s3d4.cn'
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
