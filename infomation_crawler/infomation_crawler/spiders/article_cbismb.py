# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from scrapy import FormRequest
from infomation_crawler.items import WebArticleItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ArticleCbismbSpider(Spider):
  name = "article_cbismb"
  allowed_domains = ["www.cbismb.com"]
  start_urls = [
    'http://www.cbismb.com/bigdata/list.html',
    'http://www.cbismb.com/soft/list.html',
    'http://www.cbismb.com/byod/list.html',
    'http://www.cbismb.com/cloud/list.html',
  ]

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  post_url = 'http://www.cbismb.com/common/page/ArticleList.jsp'
    
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
    return self.parse_start(response)

  def parse_start(self, response):
    match = re.match(r'.*?name="column_id" value="(\d+)"', response.body, re.DOTALL)
    if match:
      column_id = match.group(1)

    return FormRequest(self.post_url, formdata={
      'action': 'columnlist',
      'column_id': column_id,
      'p': '1',
      'pageSize': '45'}, meta={'column_id': column_id, 'p': 1}, callback=self.parse_list)

  def parse_list(self, response):

    continue_next = True

    for data in response.body.split('</ul><ul>'):
      match = re.match(r'.*<a href="(\S+)".*?class="time">(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', data)
      if match:
        news_url = 'http://www.cbismb.com' + match.group(1)

        publish_time = None
        try:
          publish_time = datetime.datetime.strptime(match.group(2), '%Y-%m-%d %H:%M:%S')
        except:
          pass

        if publish_time and publish_time.date() not in self.time_range:
          continue_next = False
          break

        yield Request(news_url, meta={'publishTime': publish_time}, callback=self.parse_news)

    if continue_next and response.meta['p'] < 10:
      yield FormRequest(self.post_url,
        formdata={
          'action': 'columnlist',
          'column_id': response.meta['column_id'],
          'p': str(response.meta['p'] + 1),
          'pageSize': '45'
        },
        meta={
          'column_id': response.meta['column_id'],
          'p': response.meta['p'] + 1
        },
      callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@id="cont_title"]/text()')
    i['url'] = response.url

    i['source'] = ''
    try:
      source = xpath.first('//*[@class="text_r_b"]/span[1]/text()')
      match = re.match(ur'来源：(\S+)', source)
      if match:
        i['source'] = match.group(1)
    except:
      pass

    i['author'] = ''
    try:
      author = xpath.first('//*[@class="text_r_t"]/span[1]/text()')
      match = re.match(ur'作者：(\S+)', author)
      if match:
        i['author'] = match.group(1)
    except:
      pass

    i['publishTime'] = str(response.meta['publishTime'].date()) if response.meta['publishTime'] else str(self.yesterday)

    i['abstract'] = ''
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@class="textcontent"]')
    i['siteName'] = 'www.cbismb.com'
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
