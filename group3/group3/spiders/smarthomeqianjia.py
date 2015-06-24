# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
from urlparse import urlparse
import datetime
import re

class SmarthomeQianjiaSpider(Spider):
  name = "smarthomeqianjia"
  allowed_domains = ["qianjia.com"]
  start_urls = [
    'http://smarthome.qianjia.com/news/'
  ]

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//*[@ id="newslistContent"]/*[@class="item img-small"]/div[@class="txtarea"]/h1/a/@href')

    domain_url = self.domain_url(response.url)

    for news_url in news_url_list:
      yield Request(news_url, callback=self.parse_news)

    next_url = xpath.first('//a[@title="' + u'下一页' + '"]/@href')
    if next_url:
      yield Request(domain_url + '/news/' + next_url, callback=self.parse_list)

  def parse_news(self, response):

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//h1[@class="title"]/text()')
    if not i['title']:
      i['title'] = xpath.first('//*[@class="detail-title"]/h1/text()')

    if not i['title']:
      return

    i['url'] = response.url

    i['source'] = xpath.first('//*[@class="author"]/a/text()')
    i['author'] = ''
    
    i['publishTime'] = None
    
    try:
      time_str = xpath.first('//*[@class="time"]/text()')
      print time_str
      match = re.match(ur'(\d+)年(\d+)月(\d+)日', time_str)
      if match:
        time_str = '20' + match.group(1) + '-' + match.group(2) + '-' + match.group(3)
        i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d')
    except:
      pass

    if not i['publishTime']:
      try:
        time_str = xpath.first('//*[@class="post-date"]/text()')
        match = re.match(ur'(\d+)年(\d+)月(\d+)日', time_str)
        if match:
          time_str = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d')
      except:
        pass

    if not i['publishTime']:
      i['publishTime'] = datetime.datetime.now()

    i['abstract'] = xpath.first('//*[@class="detail-brief"]/text()')
    if not i['abstract']:
      i['abstract'] = xpath.first('//meta[@name="description"]/@content')

    i['keyWords'] = ', '.join(xpath.list('//*[@class="wordspaste"]/a/@href'))
    i['content'] = xpath.first('//*[@id="detail-con"]')

    i['siteName'] = u'中国智能家居网'
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
