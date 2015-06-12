from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class HuxiuSpider(CrawlSpider):
  name = 'huxiu'
  allowed_domains = ['huxiu.com']
  start_urls = ['http://www.huxiu.com/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles  

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']
   
    i['author'] = ''

    content = sel.xpath('//div[@class="neirong-box"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'huxiu'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter huxiu_parse_item...."
    sel = Selector(response)
    items = []
    
    toutiao = sel.xpath('//div[@class="toutiao idx-toutiao"]')
    i = WebArticleItem()
    i['url'] = 'http://www.huxiu.com'+toutiao.xpath('h2/a/@href').extract()[0]
    title = toutiao.xpath('h2/a/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''
    abstract = toutiao.xpath('p/text()').extract()
    i['abstract'] = len(abstract)>0 and abstract[0] or ''    
    source = toutiao.xpath('div[@class="box-other"]/span[@class="source-quote"]/a/text()').extract()
    i['source'] = len(source)>0 and source[0].strip() or ''    
    pubTime = toutiao.xpath('div[@class="box-other"]/time/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
    keyWordList = toutiao.xpath('div[@class="box-other"]/span[@class="tags-box"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    items.append(i)

    newsLists = sel.xpath('//div[@class="article-list idx-list"]/div/div[@class="article-box-ctt"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://www.huxiu.com'+news.xpath('h4/a/@href').extract()[0]

      title = news.xpath('h4/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
    
      abstract = news.xpath('div[@class="article-summary"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''

      source = news.xpath('div[@class="box-other"]/span[@class="source-quote"]/a/text()').extract()
      i['source'] = len(source)>0 and source[0].strip() or ''    

      pubTime = news.xpath('div[@class="box-other"]/time/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
      
      keyWordList = news.xpath('p[@class="tags-box"]/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords

      items.append(i)
    
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
