# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import json
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

class ArticleToutiaoSpider(Spider):
  name = "article_toutiao"
  allowed_domains = ["toutiao.com"]
  start_urls = [
    'http://toutiao.com/news_tech/'
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

  def get_data_url(self, max_behot_time):
    url_pattern = 'http://toutiao.com/api/article/recent/?source=2&count=20&category=news_tech&max_behot_time=%s&utm_source=toutiao&offset=0'
    return url_pattern % max_behot_time

  def parse(self, response):
    return self.parse_start(response)

  def parse_start(self, response):
    match = re.match(r'.*\'max_behot_time\':\s*\'([\d|\.]+)\'', response.body, re.DOTALL)
    if match:
      max_behot_time = match.group(1)
      yield Request(self.get_data_url(max_behot_time), callback=self.parse_next, meta={'jump': 0})

  def parse_next(self, response):
    json_data = json.loads(response.body)
    for data in json_data['data']:
      yield Request(data['article_url'], callback=self.parse_news, meta={'abstract': data['abstract']})

    if response.meta['jump'] < 20:
      time.sleep(1)
      yield Request(self.get_data_url(json_data['next']['max_behot_time']), callback=self.parse_next, meta={'jump': response.meta['jump'] + 1})

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[@class="title"]/h1/text()')
    i['url'] = response.url
    i['source'] = '\n'.join(xpath.list('//*[@class="profile_avatar"]/a/text()')).strip()
    i['author'] = ''

    publish_time = None
    try:
      publish_time = datetime.datetime.strptime(xpath.first('//*[@class="time"]/text()'), '%Y-%m-%d %H:%M')
    except:
      pass

    if publish_time and publish_time.date() not in self.time_range:
      return

    i['publishTime'] = str(publish_time.date()) if publish_time else str(self.yesterday)
    
    i['abstract'] = response.meta['abstract']
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@class="article-content"]')
    i['siteName'] = 'toutiao.com'
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
