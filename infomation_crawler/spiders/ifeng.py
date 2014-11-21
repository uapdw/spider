from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class IfengSpider(CrawlSpider):
  name = 'ifeng'
  allowed_domains = ['ifeng.com']
  start_urls = ['http://tech.ifeng.com/listpage/6529/1/list.shtml']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    content = sel.xpath('//div[@id="main_content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'ifeng'

    author = sel.xpath('//span[@itemprop="author"]/span/text()').extract()[0:]
    i['author'] = len(author)>0 and author[0].strip() or ''
    source = sel.xpath('//span[@itemprop="publisher"]/span/text()').extract()
    i['source'] = len(source)>0 and source[0].strip() or ''
    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//p[@class="p01 ss_none"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter ifeng_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="zheng_list pl10 box"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      url = news.xpath('h1/a/@href').extract()
      i['url'] = len(url)>0 and url[0] or news.xpath('h2/a/@href').extract()[0]
      
      title = news.xpath('h1/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or news.xpath('h2/a/text()').extract()[0].strip()
      
      abstract = news.xpath('div[@class="zxbd clearfix"]/p/a/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].replace(u'[\u8be6\u7ec6]','') or ''

      pubTime = news.xpath('div[@class="Function"]/span/text()').extract()[0:]
      i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0].strip() or str(datetime.date.today())
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
