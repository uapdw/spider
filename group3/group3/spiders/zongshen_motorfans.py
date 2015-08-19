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

class ZongShenMotorfansSpider(CrawlSpider):
  name = "zongshen_motorfans"
  allowed_domains = ["www.motorfans.com.cn"]
  start_urls = [
    'http://www.motorfans.com.cn/bbs/f_245.htm'
  ]

  rules = (
    Rule(LinkExtractor(allow=('f_245_c_0_\d+.htm'))),
    Rule(LinkExtractor(allow=('t_\d+.htm')), callback='parse_thread'),
    Rule(LinkExtractor(allow=('t_\d+_\d+.htm')), callback='parse_thread'),
  )

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]

  def __init__(self,*args, **kwargs):
    super(ZongShenMotorfansSpider, self).__init__(*args, **kwargs)
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
      match = re.match('.*t_(\d+)_\d+.htm', response.url)
      if match:
        threadId = match.group(1)
      if not threadId:
        match = re.match('.*t_(\d+).htm', response.url)
        threadId = match.group(1)
    except Exception as e:
      print 'can not find threadId on url: ', response.url, '\n', e
      raise e

    selector_list = xpath.selector('//tr[starts-with(@bgcolor, "#")]')

    pair_selector_list = []
    temp_selector = None
    for index, selector in enumerate(selector_list):
      if index % 2 == 0:
        temp_selector = selector
      else:
        pair_selector_list.append((temp_selector, selector))

    for index, (up_selector, down_selector) in enumerate(pair_selector_list):
      up_xpath = XPath(up_selector)
      down_xpath = XPath(down_selector)

      i = WebBBSItem()

      i['url'] = response.url
      i['source'] = ''
      i['abstract'] = ''
      i['keyWords'] = keywords
      i['siteName'] = 'autohome.com.cn'
      i['addTime'] = datetime.datetime.now()

      i['postId'] = up_xpath.first('//*[starts-with(@name, "pid")]/@name')
      i['threadId'] = threadId

      if index == 0:
        try:
          i['title'] = xpath.first('//*[@class="header"]/.//*[@class="bold"]/text()')
        except:
          i['title'] = ''
      else:
        i['title'] = ''

      try:
        i['author'] = up_xpath.first('//a[starts-with(@href, "viewpro.php?uid=")]/text()')
      except:
        i['author'] = ''

      i['publishTime'] = None

      try:
        time_str = down_xpath.first('./td/div/text()').strip()
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass

      if i['publishTime']:
        if self.increment and i['publishTime'] not in self.time_range:
          continue
      else:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['content'] = up_xpath.first('//*[starts-with(@id, "post_content_")]')

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
