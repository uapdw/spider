# -*- coding: utf-8 -*-


__author__ = 'liufeng'

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from group3.items import WebArticleItem
import re
from urlparse import urlparse
import datetime

class Ea3wSpider(Spider):
  name = "ea3w"
  allowed_domains = ["ea3w.com"]
  start_urls = [
    'http://ac.ea3w.com/more/2_16.html',
    'http://icebox.ea3w.com/more/2_6.html',
    'http://washer.ea3w.com/more/2_11.html'
  ]

  def parse(self, response):
    return self.parse_list(response)

  def parse_list(self, response):
    xpath = XPath(Selector(response))
    news_url_list = xpath.list('//*[@class="list"]/li/h3/a/@href')
    if not news_url_list:
      yield Request(response.url, callback=self.parse_list, dont_filter=True)
    else:
      domain_url = self.domain_url(response.url)

      for news_url in news_url_list:
        yield Request(domain_url + news_url, callback=self.parse_news)

      next_url = xpath.first('//*[@class="next"]/@href')
      if next_url:
        yield Request(domain_url + next_url, callback=self.parse_list)

  def parse_news(self, response):
    domain_url = self.domain_url(response.url)

    if domain_url + '/picnews' in response.url:
      return

    xpath = XPath(Selector(response))
    i = WebArticleItem()

    i['title'] = xpath.first('//h1/text()')
    i['url'] = response.url

    author_xpath_list = ['//*[@id="author_baidu"]/text()', '//*[@class="writer"]/text()']
    for author_xpath in author_xpath_list:
      i['author'] = xpath.first(author_xpath)
      if i['author']:
        break
    match = re.match(u'作者：(\S+)', i['author'], re.UNICODE)
    if match:
      i['author'] = match.group(1)

    i['publishTime'] = None
        
    try:
      time_str = xpath.first('//*[@id="pubtime_baidu"]/text()')
      if time_str:
        match = re.match(u'时间：(.+)', time_str, re.UNICODE)
        if match:
          time_str = match.group(1)
          i['publishTime'] = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    except:
      pass

    if not i['publishTime']:
      try:
        time_str = xpath.first('//*[@class="date"]/text()')
        match = re.match(ur'(\d+)月(\d+)日', time_str)
        if match:
          time_str = str(match.group(1) + '-' + match.group(2))
          i['publishTime'] = datetime.datetime.strptime(time_str, '%m-%d')
      except:
        pass

    if not i['publishTime']:
      i['publishTime'] = datetime.datetime.now()

    source_xpath_list = ['//*[@class="source"]/text()', '//*[@id="source_baidu"]/a/text()', '//*[@id="source_baidu"]/text()']
    for source_xpath in source_xpath_list:
      i['source'] = xpath.first(source_xpath)
      if i['source']:
        break

    match = re.match(u'来源：(\S+)', i['source'], re.UNICODE)
    if match:
      i['source'] = match.group(1)

    abstract_xpath_list = ['//*[@class="intro-module clearfix"]/p[3]/text()', '//*[@name="description"]/@content']
    for abstract_xpath in abstract_xpath_list:
      i['abstract'] = xpath.first(abstract_xpath)
      if i['abstract']:
        break
    if not i['abstract']:
      i['abstract'] = xpath.first('//*[@name="description"]')
      match = re.match('content="(.*)">', i['abstract'])
      if match:
        i['abstract'] = match.group(1)

    i['keyWords'] = xpath.first('//*[@name="keywords"]/@content')

    content_xpath_list = ['//*[@id="main_content"]', '//*[@class="at-text"]']
    for content_xpath in content_xpath_list:
      i['content'] = xpath.first(content_xpath)
      if i['content']:
        break

    i['siteName'] = u'万维家电网'
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
