# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
import re
from urlparse import urlparse
import datetime
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class Hc360Spider(Spider):
  name = "hc360"
  allowed_domains = ["hc360.com"]
  start_urls = [
    'http://info.homea.hc360.com/list/zx_bsjd_binx.shtml',
    'http://info.homea.hc360.com/list/zx_bsjd_kt.shtml',
    'http://info.homea.hc360.com/list/zx_bsjd_xiyiji.shtml'
  ]

  more_url = 'http://www.homea.hc360.com'

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
    return self.parse_front(response)

  def parse_front(self, response):
    request_list = []

    domain_url = self.domain_url(response.url)

    xpath = XPath(Selector(response))
    page_url_list = xpath.list('//table[2]/tr/td/a/@href')
    for page_url in page_url_list[:3]: # 前三页（算本页）
      if page_url != self.more_url:
        request_list.append(Request(domain_url + '/list/' + page_url, callback=self.parse_list))

    request_list.extend(self.parse_list(response))

    return request_list

  def parse_list(self, response):
    xpath = XPath(Selector(response))

    domain_url = self.domain_url(response.url)

    news_url_list = xpath.list('//table[1]/tr/td/a/@href')
    for news_url in news_url_list:
      match = re.match('/\d+/\d+/\d+.shtml', news_url)
      if match:
        print 'list::::' + domain_url + news_url
        yield Request(domain_url + news_url, callback=self.parse_news)


  def parse_news(self, response):
    xpath = XPath(Selector(response))

    if 'item' not in response.meta:
      i = WebArticleItem()

      i['title'] = xpath.first('//*[@id="title"]/h1/text()')
      i['url'] = response.url

      i['author'] = xpath.first('//*[@id="endAuthor"]/text()')
      match = re.match(u'作者：(\S+)', i['author'], re.UNICODE)
      if match:
        i['author'] = match.group(1)

      i['publishTime'] = None
        
      try:
        time_str = xpath.first('//*[@id="endData"]/text()')
        match = re.match(u'(\d+)年(\d+)月(\d+)日(\d+):(\d+)', time_str, re.UNICODE)
        if match:
          time_str = match.group(1) + '-' + match.group(2) + '-' + match.group(3) + ' ' + match.group(4) + ':' + match.group(5)
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
      except:
        pass

      if not i['publishTime']:
        i['publishTime'] = datetime.datetime(1970,1,1)

      i['source'] = xpath.first('//*[@id="endSource"]/text()')
      if not i['source']:
        i['source'] = xpath.first('//*[@id="endSource"]/.//*/text()')
      match = re.match(u'来源：(.+)', i['source'], re.UNICODE)
      if match:
        i['source'] = match.group(1)

      i['abstract'] = xpath.first('//*[@name="description"]/@content')
      i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')
      i['content'] = '\r\n'.join(xpath.list('//*[@id="artical"]/p'))

      i['siteName'] = u'慧聪家电网'
      i['newstype'] = u'家电'
      i['addTime'] = datetime.datetime.now()
    else:
      i = response.meta['item']
      i['content'] += '\r\n' + '\r\n'.join(xpath.list('//*[@id="artical"]/p'))

    next_url = xpath.first('//*[@ id="pageno"]/a[text()="' + u'下一页' + '"]/@href')
    if next_url:
      url_front = i['url'][:i['url'].rfind('/') + 1]
      return Request(url_front + next_url, callback=self.parse_news)
    else:
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
