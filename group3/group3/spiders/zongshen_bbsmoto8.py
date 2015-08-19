# -*- coding: utf-8 -*-

__author__ = 'liufeng'

import datetime
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from group3.items import WebBBSItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

# 写入bbsnew列族

class ZongShenBBSMoto8Spider(CrawlSpider):
  name = "zongshen_bbsmoto8"
  allowed_domains = ["bbs.moto8.com"]

  start_urls = [
    'http://bbs.moto8.com/forum-798-1.html'
  ]

  rules = (
    Rule(LinkExtractor(allow=('forum-798-\d+.html'), restrict_xpaths=('//*[@class="nxt"]'))), #前9页
    Rule(LinkExtractor(allow=('thread-\d+-\d+-\d+.html')), callback='parse_thread'),
  )

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]
    
  def __init__(self,*args, **kwargs):
    super(ZongShenBBSMoto8Spider, self).__init__(*args, **kwargs)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_thread(self, response):

    xpath = XPath(Selector(response))

    # 公共变量
    keywords = xpath.first('//*[@name="keywords"]/@content') # 所有item的keywords相同

    threadId = None
    try:
      match = re.match('.*thread-(\d+)-\d+-\d+.html', response.url)
      threadId = match.group(1)
    except Exception as e:
      print 'can not find threadId on url: ', response.url, '\n', e
      raise e

    for index, selector in enumerate(xpath.selector('//*[starts-with(@id, "post_")]')):
      post_xpath = XPath(selector)

      i = WebBBSItem()

      i['url'] = response.url
      i['source'] = ''
      i['abstract'] = ''
      i['keyWords'] = keywords
      i['siteName'] = 'bbs.moto8.com'
      i['addTime'] = datetime.datetime.now()

      i['postId'] = post_xpath.first('@id')
      i['threadId'] = threadId

      if index == 0:
        try:
          i['title'] = xpath.first('//*[@id="thread_subject"]/text()')
        except:
          i['title'] = ''
      else:
        i['title'] = ''

      try:
        i['author'] = post_xpath.first('//*[@class="authi"]/*[starts-with(@href, "space-uid-")]/text()')
      except:
        i['author'] = ''

      i['publishTime'] = None

      try:
        time_str = post_xpath.first('//*[starts-with(@id, "authorposton")]/text()')
        match = re.match(u'发表于 (\d+-\d+-\d+ \d+:\d+)', time_str)
        time_str = match.group(1)
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass

      if not i['publishTime']:
        try:
          time_str = post_xpath.first('//*[starts-with(@id, "authorposton")]/span/@title')
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        except:
          pass

      if i['publishTime']:
        if self.increment and i['publishTime'] not in self.time_range:
          continue
      else:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['content'] = post_xpath.first('//*[starts-with(@id, "postmessage_")]')

      yield i

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
