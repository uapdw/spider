# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time

from urllib import quote_plus

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
  
class ArticleMyzakerSpider(Spider):
  name = "article_myzaker"
  allowed_domains = ["app.myzaker.com"]
  start_urls = [
    'http://app.myzaker.com/index.php?app_id=13'
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

    
  def get_next_url(self, next_url):
    ret = 'http://app.myzaker.com/news/next.php?url=' + quote_plus(next_url) + '&f=&_version=4.3'
    return ret

  def parse(self, response):
    return self.parse_start(response)
    # yield Request('http://app.myzaker.com/news/article.php?pk=55dbecfb9490cb7744000027', self.parse_news)

  def parse_start(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//a[starts-with(@href, "http://app.myzaker.com/news/article.php?pk=")]/@href')
    for news_url in news_url_list:
      yield Request(news_url, callback=self.parse_news)

    match = re.match(r'.*?var\s*next_url\s*=\s*"(\S+?)";', response.body, re.DOTALL)
    if match:
      next_url = self.get_next_url(match.group(1))
      yield Request(next_url, callback=self.parse_next)

  def parse_next(self, response):
    url_list = re.findall(r'<a href=\\"(\S+)\\"', response.body)
    for url in url_list:
      url = re.sub(r'\\/', '/', url)
      if re.match(r'http://app\.myzaker\.com/news/article\.php\?pk=[\d|\w]+', url):
        yield Request(url, callback=self.parse_news)

    match = re.match(r'.*"next_url":"(\S+?)"', response.body, re.DOTALL)
    if match:
      next_url = self.get_next_url(re.sub(r'\\/', '/', match.group(1)))
      yield Request(next_url, callback=self.parse_next)

  def parse_news(self, response):

    if 'http://app.myzaker.com/news/article.php?pk=' not in response.url:
      return

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//*[contains(@id, "titleContent")]/text()')
    i['url'] = response.url
    i['source'] = xpath.first('//*[contains(@id, "AuthorAndTime")]/text()')
    i['author'] = ''

    publish_time = None
    publish_time_str = xpath.first('//*[contains(@id, "AuthorAndTime")]/span/text()')
   
    match = re.match(ur'(\d+)(\S+)前', publish_time_str)
    if match:
      publish_time = datetime.datetime.now()
      number = match.group(1)
      unit = match.group(2)
      if u'分' in unit:
        publish_time = publish_time - datetime.timedelta(minutes=int(number))
      elif u'时' in unit:
        publish_time = publish_time - datetime.timedelta(hours=int(number))
      elif u'天' in unit:
        publish_time = publish_time - datetime.timedelta(days=int(number))

    if not publish_time:
      match = re.match(r'(\d+)-(\d+)', publish_time_str)
      if match:
        publish_time = datetime.datetime(datetime.datetime.now().year, int(match.group(1)), int(match.group(2)))

    if not publish_time and u'昨天' in publish_time_str:
      publish_time = datetime.datetime.now()
      publish_time = publish_time - datetime.timedelta(days=1)

    if not publish_time and u'前天' in publish_time_str:
      publish_time = datetime.datetime.now()
      publish_time = publish_time - datetime.timedelta(days=2)

    i['publishTime'] = str(publish_time.date()) if publish_time else str(self.yesterday)

    i['abstract'] = ''
    i['keyWords'] = xpath.first('//meta[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[@id="content_text"]')
    i['siteName'] = 'app.myzaker.com'
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
