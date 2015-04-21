from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from group3.items import WebArticleItem
from scrapy.http import Request
import json
import datetime
import pymongo

class BaiduBaijiaSpider(CrawlSpider):
  name = 'baidubaijia'
  allowed_domains = ['baidu.com']
  start_urls = ['http://baijia.baidu.com/?tn=listarticle&labelid=2']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    author = sel.xpath('//div[@class="article-author-time"]/a/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    pubTime = sel.xpath('//div[@class="article-author-time"]/span/text()').extract()
    pubTime = len(pubTime)>0 and pubTime[0].strip().split()[0].replace(u'\u6708','-').replace(u'\u65e5','') or ''
    i['publishTime'] = len(pubTime)>0 and str(yesterday.year)+'-'+pubTime or str(datetime.date.today())
    if cmp(i['publishTime'],str(yesterday))!=0:
      return
    source = sel.xpath('//div[@class="article-info"]/div[4]/a/text()').extract()
    i['source'] = len(source)>0 and source[0] or ''

    content = sel.xpath('//div[@class="article-detail"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'baijia.baidu'
    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@class="article-tags"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse_json(self, response):
    sel = Selector(response)
    jsonresponse = json.loads(response.body_as_unicode())
    
    items = []
    newsLists = jsonresponse['data']['list']
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news['m_display_url']
      
      title = news['m_title']
      i['title'] = len(title)>0 and title.strip() or ''
      
      abstract = news['m_summary']
      i['abstract'] = len(abstract)>0 and abstract.strip() or ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)

  def parse(self, response):
    print "enter baijia.baidu_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="feeds"]/div/div')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h3/a/@href').extract()[0]
      
      title = news.xpath('h3/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('p/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)

    yield Request('http://baijia.baidu.com/ajax/labellatestarticle?page=2&pagesize=20&labelid=2&prevarticalid=36966',callback=self.parse_json)
    yield Request('http://baijia.baidu.com/ajax/labellatestarticle?page=3&pagesize=20&labelid=2&prevarticalid=36944',callback=self.parse_json)
