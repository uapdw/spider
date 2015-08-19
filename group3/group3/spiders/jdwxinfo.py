# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from group3.items import WebBBSItem
from urlparse import urlparse
import datetime
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class JdwxInfoSpider(CrawlSpider):
  name = "jdwxinfo"
  allowed_domains = ["www.jdwx.info", "so.jdwx.info"]
  start_urls = [
    'http://www.jdwx.info/forum-44-1.html',
    'http://www.jdwx.info/forum-15-1.html',
    'http://www.jdwx.info/forum-16-1.html'
  ]

  rules = (
    Rule(LinkExtractor(allow=('forum-44-\d.html'), restrict_xpaths=('//*[@class="nxt"]'))), #前9页
    Rule(LinkExtractor(allow=('forum-15-\d.html'), restrict_xpaths=('//*[@class="nxt"]'))), #前9页
    Rule(LinkExtractor(allow=('forum-16-\d.html'), restrict_xpaths=('//*[@class="nxt"]'))), #前9页
    Rule(LinkExtractor(allow=('thread-\d+-1-\d+.html')), callback='parse_thread'),
  )
    
  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  def __init__(self,**kw):
    super(JdwxInfoSpider,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_thread(self, response):

    threadId = None
    try:
      match = re.match('.*thread-(\d+)-1-\d+.html', response.url)
      if match:
        threadId = match.group(1)
      if not threadId:
        match = re.match('.*mod=viewthread&tid=(\d+)', response.url)
        threadId = match.group(1)
    except Exception as e:
      print 'can not find threadId on url: ', response.url, '\n', e
      raise e
        
    xpath = XPath(Selector(response))
    i = WebBBSItem()

    i['title'] = xpath.first('//*[@id="thread_subject"]/text()')
    if not i['title']: # 需要一定权限才能流量
      return

    i['author'] = xpath.first('//*[@ id="postlist"]/div[starts-with(@id, "post_")][1]/.//td[1]/.//*[@class="authi"]/a/text()')
    if not i['author']: # 用户被删除
      return

    i['url'] = response.url
    
    i['threadId'] = threadId
    i['postId'] = xpath.first('//*[@ id="postlist"]/div[starts-with(@id, "post_")][1]/@id')

    i['source'] = ''

    i['publishTime'] = None

    try:
      time_str = xpath.first('//*[starts-with(@id, "authorposton")]/text()')
      match = re.match(u'发表于\s+(\d+-\d+-\d+ \d+:\d+)', time_str, re.UNICODE)
      if match:
        time_str = match.group(1)
      i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    except:
      pass

    if not i['publishTime']:
      try:
        time_str = xpath.first('//*[starts-with(@id, "authorposton")]/span/@title')
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
      except:
        pass
    
    if i['publishTime']:
      if i['publishTime'].date() not in self.time_range:
        return
    else:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['abstract'] = ''
    i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')
    i['content'] = xpath.first('//*[starts-with(@id, "postmessage_")]')

    i['siteName'] = 'www.jdwx.info'
    i['addTime'] = datetime.datetime.now()

    return i

  def domain_url(self, url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain

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
