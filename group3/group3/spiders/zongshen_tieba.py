# -*- coding: utf-8 -*-


__author__ = 'liufeng'

import datetime
import re
import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from group3.items import WebBBSItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class ZongshenTiebaSpider(CrawlSpider):
  name = "zongshen_tieba"
  allowed_domains = ["tieba.baidu.com"]
  start_urls = [
    'http://tieba.baidu.com/f?kw=%E5%AE%97%E7%94%B3&ie=utf-8'
  ]

  rules = (
    Rule(LinkExtractor(allow=('.*'), restrict_xpaths=('//*[@class="next"]'))),
    Rule(LinkExtractor(allow=('/p/\d+')), callback='parse_thread'),
  )

  increment = False
  if increment:
    today = datetime.date.today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1))
    time_range = [today, yesterday]
    
  def __init__(self,*args, **kwargs):
    super(ZongshenTiebaSpider, self).__init__(*args, **kwargs)
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

    threadId = None
    try:
      match = re.match('.*p/(\d+)', response.url)
      threadId = match.group(1)
    except Exception as e:
      print 'can not find threadId on url: ', response.url, '\n', e
      raise e

    for index, selector in enumerate(xpath.selector('//*[contains(@class, "l_post_bright")]')):
      post_xpath = XPath(selector)

      i = WebBBSItem()

      i['url'] = response.url
      i['source'] = ''
      i['abstract'] = ''
      i['keyWords'] = ''
      i['siteName'] = 'tieba.baidu.com'
      i['addTime'] = datetime.datetime.now()

      data_field = post_xpath.first('@data-field')
      data_dict = json.loads(data_field)

      i['postId'] = str(data_dict['content']['post_id'])
      i['threadId'] = threadId

      if index == 0:
        try:
          i['title'] = xpath.first('//*[starts-with(@class, "core_title_txt")]/@title')
        except:
          i['title'] = ''
      else:
        i['title'] = ''

      try:
        i['author'] = data_dict['author']['user_name']
      except:
        i['author'] = ''

      i['publishTime'] = None

      try:
        time_str = data_dict['content']['date']
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass

      if i['publishTime']:
        if self.increment and i['publishTime'] not in self.time_range:
          continue
      else:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['content'] = post_xpath.first('//*[starts-with(@id, "post_content")]')

      yield i

    for selector in xpath.selector('//*[contains(@class, "core_reply_content")]/ul/li'):
      subpost_xpath = XPath(selector)

      if '{total_num' in subpost_xpath.first('@data-field'):
        continue

      i = WebBBSItem()

      i['url'] = response.url
      i['source'] = ''
      i['abstract'] = ''
      i['keyWords'] = ''
      i['siteName'] = 'tieba.baidu.com'
      i['addTime'] = datetime.datetime.now()

      data_field = subpost_xpath.first('@data-field')
      data_field = re.sub('\'', '"', data_field)
      data_dict = json.loads(data_field)

      i['postId'] = str(data_dict['pid']) + '_' + str(data_dict['spid'])
      i['threadId'] = threadId
      i['title'] = ''

      try:
        i['author'] = data_dict['user_name']
      except:
        i['author'] = ''

      i['publishTime'] = None

      try:
        time_str = subpost_xpath.first('//*[@class="lzl_time"]/text()')
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass

      if i['publishTime']:
        if self.increment and i['publishTime'] not in self.time_range:
          continue
      else:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['content'] = post_xpath.first('//*[@class="lzl_content_main"]')

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
