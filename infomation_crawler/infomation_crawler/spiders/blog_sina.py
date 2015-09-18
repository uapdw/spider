# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from infomation_crawler.items import WebBlogItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class BlogSinaSpider(Spider):
  name = "blog_sina"
  allowed_domains = ["search.sina.com.cn","blog.sina.com.cn"]
  start_urls = [
    'http://search.sina.com.cn/?q=%D3%C3%D3%D1&c=blog&from=index'
  ]

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  the_day_before_yesterday = (datetime.date.today() - datetime.timedelta(days=2))
  time_range = [today, yesterday, the_day_before_yesterday]
    
  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebBlogs = infoDB.web_blogs
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
    news_url_list = xpath.list('//*[@class="result-boxes"]/div/h2/a/@href')
    time_list = xpath.list('//*[@class="result-boxes"]/div/div/div/p[2]/span[@class="fgray_time"]/text()')

    continue_next = True

    for news_url, time_str in zip(news_url_list, time_list):
      publish_time = None

      try:
        publish_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
      except:
        pass

      if publish_time and publish_time.date() not in self.time_range:
        continue_next = False
        break

      yield Request(news_url, callback=self.parse_news, meta={'publishTime': publish_time})

    if continue_next:
      next_url = 'http://search.sina.com.cn/' + xpath.first(u'//*[@title="下一页"]/@href')
      if next_url:
        yield Request(next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebBlogItem()

    i['title'] = xpath.first('//h1[@class="h1_tit"]/text()')
    if not i['title']:
      i['title'] = '\n'.join(xpath.list('//*[@class="articalTitle"]/h2//text()')).strip()

    i['url'] = response.url
    i['source'] = ''
    i['author'] = ''
    i['publishTime'] = response.meta['publishTime']
    i['publishTime'] = str(i['publishTime'].date()) if i['publishTime'] else str(self.yesterday)
    i['abstract'] = xpath.first('//meta[@name="description"]/@content')
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@id="articlebody"]')
    i['siteName'] = 'blog.sina.com.cn'
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
