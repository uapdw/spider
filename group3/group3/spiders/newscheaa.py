# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
import re
import datetime

class NewsCheaaSpider(Spider):
  name = "newscheaa"
  allowed_domains = ["cheaa.com"]
  start_urls = [
    'http://news.cheaa.com/hangye.shtml'
  ]

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//*[@id="main-list"]/div[contains(@class,"ListPageBox")]/.//a/@href')
    for news_url in news_url_list:
      yield Request(news_url, callback=self.parse_news)

    next_url = xpath.first('//a[@class="next"]/@href')
    if next_url:
      yield Request(next_url, callback=self.parse_list)

  def parse_news(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()
    i['title'] = xpath.first('//*[@id="NewsTitle"]/h1/text()')
    i['url'] = response.url

    i['publishTime'] = None
    
    news_info = xpath.first('//*[@id="NewsInfo"]/text()')
    match = re.match(u'(\d\d\d\d-\d\d-\d\d \d\d:\d\d).*:\s+(\S+)\s+(\S+)', news_info, re.UNICODE)
    if match:
      time_str = match.group(1)
      i['source'] = match.group(2)
      i['author'] = match.group(3)
    else:
      match = re.match(u'(\d\d\d\d-\d\d-\d\d \d\d:\d\d).*:\s+(\S+)', news_info, re.UNICODE)
      if match:
        time_str = match.group(1)
        try:
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        except:
          pass
        i['source'] = match.group(2)
        i['author'] = ''
      else:
        i['source'] = ''
        i['author'] = ''

    if not i['publishTime']:
      i['publishTime'] = datetime.datetime.now()

    
    i['abstract'] = xpath.first('//*[@name="description"]/@content')
    i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')
    i['siteName'] = u'中国家电信息网'
    i['content'] = xpath.first('//*[@id="ctrlfscont"]')
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
