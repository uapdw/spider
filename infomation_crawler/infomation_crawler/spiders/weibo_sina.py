# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import re
import datetime
import time
from urllib import quote

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider
from infomation_crawler.items import WeiboItem

import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class WeiboSinaSpider(CrawlSpider):
  name = 'weibo_sina'
  allowed_domains = ['zhongsou.com']

  url_pattern = u'http://t.zhongsou.com/wb?w=%s&form_id=1&v=%s'

  keywords = [u'用友']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWeiBo = infoDB.web_articles
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
    for keyword in self.keywords:
      url = self.url_pattern % (quote(keyword.encode('gbk')), quote(u'中搜'.encode('gbk')))
      yield Request(url)

  def parse(self, response):
    xpath = XPath(Selector(text=response.body.decode('gb18030')))
    newsurl = xpath.selector('//div[@class="main_scenery_left"]/div[@class="godreply_on"]/div[@class="weibo_item clearfix"]')
    articles = []
    for news in newsurl:
      i = WeiboItem()
      inner_xpath = XPath(news)
      i['content'] = ''.join(inner_xpath.list('.//*[@class="weibo_txt"]/.//text()'))
      i['comments_count'] = '0'

      publish_time_str = inner_xpath.first('.//*[@class="weibo_time"]/text()')

      publish_time = None
      if not publish_time:
        match = re.match(ur'(\d+)月(\d+)日', publish_time_str)
        if match:
          publish_time = datetime.datetime(datetime.datetime.now().year, int(match.group(1)), int(match.group(2)))

      if not publish_time and u'今天' in publish_time_str:
        publish_time = datetime.datetime.now()

      if not publish_time and u'昨天' in publish_time_str:
        publish_time = datetime.datetime.now()
        publish_time = publish_time - datetime.timedelta(days=1)

      if not publish_time and u'前天' in publish_time_str:
        publish_time = datetime.datetime.now()
        publish_time = publish_time - datetime.timedelta(days=2)

      i['created_at'] = str(publish_time.date()) if publish_time else ''

      i['user_id'] = ''
      i['reposts_count'] = '0'
      i['screen_name'] = inner_xpath.first('div[@class="weibo_right"]/h3/a/text()')
      i['weibo_url'] = inner_xpath.first('.//*[@class="sina_weibo"]/@href')
      i['user_url'] = inner_xpath.first('.//*[@class="weibo_title"]/a/@href')
      i['user_icon'] = inner_xpath.first('.//*[@class="weibo_touxiang"]/a/img/@src')

      articles.append(i)
    return articles

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
