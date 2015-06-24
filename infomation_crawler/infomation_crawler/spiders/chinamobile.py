from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class ChinamobileSpider(CrawlSpider):
  name = 'chinamobile'
  allowed_domains = ['chinamobile.com']
  start_urls = ['http://labs.chinamobile.com/news/all']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    info = sel.xpath('//div[@class="l mt_5"]/text()').extract()
    newsInfo = len(info)>0 and info[0].split('|') or ''
    i['source'] = len(newsInfo)>1 and newsInfo[0].strip() or ''
    i['publishTime'] = len(newsInfo)>1 and newsInfo[-1].split()[0].strip() or str(datetime.date.today())
    i['author'] = ''

    abstract = sel.xpath('//div[@class="page_su mt_10"]/text()').extract()
    i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''
    
    content = sel.xpath('//div[@class="contentarea mt_10"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'chinamobile'

    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@class="page_mess mt_5"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter chinamobile_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@id="news_list"]/ul/li')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://labs.chinamobile.com'+news.xpath('a/@href').extract()[0]
      
      title = news.xpath('a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
