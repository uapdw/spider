from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class dsjSpider(CrawlSpider):
  name = 'dsj'
  allowed_domains = ['36dsj.com']
  start_urls = ['http://www.36dsj.com/archives/category/big-data-investment', 'http://www.36dsj.com/archives/category/bigdata']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    content = sel.xpath('//div[@class="content"]/article[@class="article-content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = '36dsj'

    source = sel.xpath('//ul[@class="article-meta"]/li[3]/a/text()').extract()
    i['source'] = len(source)>0 and source[0] or ''
    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@class="content"]/div[@class="article-tags"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter 36dsj_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="content"]/article[@class="excerpt"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h2/a/@href').extract()[0]
      
      title = news.xpath('h2/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('p[@class="note"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''

      info = news.xpath('p[@class="info"]/text()').extract()[0:]
      i['author'] = len(info)>0 and info[0].strip() or ''
      i['publishTime'] = len(info)>1 and info[1].strip() or str(datetime.date.today())
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
