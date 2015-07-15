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

class CenaSpider(Spider):
  name = "cena"
  allowed_domains = ["cena.com.cn"]
  start_urls = [
    'http://jydq.cena.com.cn/node_374.htm',
    'http://jydq.cena.com.cn/node_377.htm',
    'http://jydq.cena.com.cn/node_384.htm'
  ]

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
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//*[@id="list"]/ul/li/a/@href')

    domain_url = self.domain_url(response.url)

    for news_url in news_url_list:
      if '://' not in news_url:
        news_url = domain_url + '/' + news_url
      yield Request(news_url, callback=self.parse_news)

    next_url = xpath.first('//*[@id="displaypagenum"]/.//a[text()="' + u'下一页' + '"]/@href')
    if next_url:
      yield Request(domain_url + '/' + next_url, callback=self.parse_list)

  def parse_news(self, response):
    # domain_url = self.domain_url(response.url)

    # if domain_url + '/picnews' in response.url:
    #   return

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//h1[@class="artTitle"]/text()')
    i['url'] = response.url

    i['source'] = xpath.first('//*[@class="media_name left"]/text()')
    match = re.match(u'\s*(\S*)\s*作者：(.*)', i['source'], re.UNICODE)
    if match:
      i['author'] = match.group(2)
      i['source'] = match.group(1)
    else:
      i['author'] = ''

    try:
      time_str = xpath.first('//*[@class="pub_date left"]/text()')
      match = re.match(u'发布时间：(.+)', time_str, re.UNICODE)
      if match:
        time_str = match.group(1)
      i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d')
    except:
      i['publishTime'] = datetime.datetime(1970,1,1)

    i['abstract'] = xpath.first('//*[@name="Description"]/@content')
    if not i['abstract']:
      # 取第一个非空行
      p_list = xpath.list('//*[@id="artbody"]/p/text()')
      for p in p_list:
        p = p.strip()
        if p:
          i['abstract'] = p

    i['keyWords'] = xpath.first('//*[@name="Keywords"]/@content')
    i['content'] = xpath.first('//*[@id="artbody"]')

    i['siteName'] = u'电子信息产业网'
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
