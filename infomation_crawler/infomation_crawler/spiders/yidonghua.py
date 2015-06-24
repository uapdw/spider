from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
import re

class YidonghuaSpider(CrawlSpider):
  name = 'yidonghua'
  allowed_domains = ['yidonghua.com']
  start_urls = ['http://www.yidonghua.com/mobilepoint','http://www.yidonghua.com/mobiledynamics']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    content = sel.xpath('//div[@class="entry clearfix"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'yidonghua'

    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter yidonghua_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="wrap-post"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('div/h2[@class="title"]/a/@href').extract()[0]
      
      title = news.xpath('div/h2[@class="title"]/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('div/div[@class="entry clearfix"]/p').extract()
      i['abstract'] = len(abstract)>1 and re.sub(r'<(.*?)>','',abstract[1]) or ''

      i['author'] = ''
      pubTime = news.xpath('div/div[@class="postmeta-date"]/span/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0].strip().replace('/','-') or str(datetime.date.today())

      keyWordList = news.xpath('div/div[@class="postmeta-secondary"]/span[@class="meta_tags"]/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords.replace(u'\uff0c','|')
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
