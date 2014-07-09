# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import BaiduNewsItem
import re
import datetime
import pymongo

class BaiduNewsSpider(Spider):
  name = "baidu"
  allowed_domains = ['baidu.com']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tKeywords = infoDB.keywords
  listKeywords = tKeywords.find()
  urls = []

  for item in listKeywords:
    keyword = item['keyword']
    url = "http://news.baidu.com/ns?ct=0&rn=100&ie=utf-8&bs=" + keyword + "&rsv_bp=1&sr=0&cl=2&f=8&prevct=1&word=" + keyword + "&tn=newstitle&inputT=0"
    urls.append(url)

  start_urls = urls

  # start_urls = [
  #   "http://news.baidu.com/ns?ct=0&rn=100&ie=utf-8&bs=大数据&rsv_bp=1&sr=0&cl=2&f=8&prevct=1&word=大数据&tn=newstitle&inputT=0"
  # ]

  def parse(self, response):
    sel = Selector(response)
    pageUrls = sel.xpath('//p[@id="page"]/a[not(@class)]/@href').extract()
    pageUrls.append(response.url)

    for url in pageUrls:
      yield Request('http://news.baidu.com' + url, self.parse_item)



  def parse_item(self, response):
    sel = Selector(response)

    sites = sel.xpath("//li[@class='result title']")
    reA = re.compile('</?\w+[^>]*>')
    items = []

    for site in sites:
      title = []
      siteName = []
      postTime = []

      titleStr = site.xpath("h3/a").extract()
      title.append(reA.sub('',titleStr[0]))

      siteStr = site.xpath("span/text()").extract()
      siteStrList = siteStr[0].replace(u'\xa0',u' ').split(' ')
      siteName.append(siteStrList[1])
      postTime.append(datetime.datetime.strptime(siteStrList[2] + ' ' + siteStrList[3],'%Y-%m-%d %H:%M:%S'))

      item = BaiduNewsItem()
      item["title"] = title
      item["href"] = site.xpath("h3/a/@href").extract()
      item["sitename"] = siteName
      item["posttime"] = postTime
      items.append(item)
      
    return items




