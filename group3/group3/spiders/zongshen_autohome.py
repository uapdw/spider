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

class ZongShenAutohomeSpider(CrawlSpider):
  name = "zongshen_autohome"
  allowed_domains = ["sou.autohome.com.cn", "club.autohome.com.cn"]

  start_urls = [
    'http://sou.autohome.com.cn/luntan?q=%d7%da%c9%ea&class=0&sort=New&pvareaid=100834&clubSearchType=0&clubSearchTime=0&entry=44&IsSelect=0&ClubClassBefore=0&error=0'
  ]

  rules = (
    Rule(LinkExtractor(allow=('.*'), restrict_xpaths=('//*[text()="' + u'下一页' + '"]'))),
    Rule(LinkExtractor(allow=('thread-o-\d+-\d+-\d+.html')), callback='parse_thread'),
  )

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]
    
  def __init__(self,*args, **kwargs):
    super(ZongShenAutohomeSpider, self).__init__(*args, **kwargs)
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
      match = re.match('.*o-\d+-(\d+)-\d+.html', response.url)
      threadId = match.group(1)
    except Exception as e:
      print 'can not find threadId on url: ', response.url, '\n', e
      raise e

    for selector in xpath.selector('//*[starts-with(@id, "F")]'):
      post_xpath = XPath(selector)

      i = WebBBSItem()

      i['url'] = response.url
      i['source'] = ''
      i['abstract'] = ''
      i['keyWords'] = keywords
      i['siteName'] = 'autohome.com.cn'
      i['addTime'] = datetime.datetime.now()

      i['postId'] = post_xpath.first('@id')
      i['threadId'] = threadId

      if i['postId'] == 'F0':
        try:
          i['title'] = post_xpath.first('//*[@class="rtitle"]/*[@class="maxtitle"]/text()')
        except:
          i['title'] = ''
      else:
        i['title'] = ''

      try:
        i['author'] = post_xpath.first('//*[@xname="uname"]/@title')
      except:
        i['author'] = ''

      i['publishTime'] = None

      try:
        time_str = post_xpath.first('@data-time')
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S')
      except:
        pass

      if i['publishTime']:
        if self.increment and i['publishTime'] not in self.time_range:
          continue
      else:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['content'] = post_xpath.first('//*[@class="rconten"]')

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
