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
  tArticles = infoDB.baidu_articles
  listKeywords = tKeywords.find()
  urls = []

  for item in listKeywords:
    keyword = item['keyword']
    #url = "http://news.baidu.com/ns?ct=0&rn=100&ie=utf-8&bs=" + keyword + "&rsv_bp=1&sr=0&cl=2&f=8&prevct=1&word=" + keyword + "&tn=newstitle&inputT=0"
    url = "http://news.baidu.com/ns?word=" + keyword + "&pn=0&cl=2&ct=1&tn=news&rn=100&ie=utf-8&bt=0&et=0"
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

    sites = sel.xpath("//li[@class='result']")
    reHtml = re.compile('</?\w+[^>]*>')
    reP = re.compile('<\s*p[^>]*>[^<]*<\s*/\s*p\s*>',re.I)
    reA = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>',re.I)
    items = []

    for site in sites:
      title = []
      siteName = []
      postTime = []
      content = []

      titleStr = site.xpath("h3/a").extract()
      title.append(reHtml.sub('',titleStr[0]))

      siteStr = site.xpath("div[@class='c-summary c-row c-gap-top-small']/div[@class='c-span18 c-span-last']/p[@class='c-author']/text()").extract()
      if len(siteStr) < 1:
	siteStr = site.xpath("div[@class='c-summary c-row ']/p[@class='c-author']/text()").extract()

      siteStrList = siteStr[0].replace(u'\xa0',u' ').split(' ')
      siteName.append(siteStrList[0])
      detailStr = site.xpath("div[@class='c-summary c-row ']").extract()
      if len(detailStr) < 1:
	detailStr = site.xpath("div[@class='c-summary c-row c-gap-top-small']").extract()
      detail = reP.sub('',detailStr[0])
      detail = reA.sub('',detail)
      content.append(reHtml.sub('',detail))
      postTime.append(datetime.datetime.strptime(siteStrList[2],'%Y-%m-%d'))

      item = BaiduNewsItem()
      item["title"] = title
      item["url"] = site.xpath("h3/a/@href").extract()
      item["sitename"] = siteName
      item["publishtime"] = postTime
      item["content"] = content
      item["addtime"] = datetime.datetime.now()
      item["keywords"] = ''
      items.append(item)
      
    return items
