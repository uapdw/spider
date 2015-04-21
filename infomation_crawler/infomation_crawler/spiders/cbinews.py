from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
from scrapy.http import FormRequest
import datetime
import pymongo

class CbinewsSpider(CrawlSpider):
  name = 'cbinews'
  allowed_domains = ['cbinews.com']
  start_urls = ['http://www.cbinews.com/cloud/list.html?id=665','http://www.cbinews.com/bigdata/list.html?id=669','http://www.cbinews.com/software/list.html?id=136']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']
    
    info = sel.xpath('//div[@class="text_r"]/div[@class="text_r_t"]/span/text()').extract()
    i['author'] = len(info)>0 and info[0].replace(u'\u4f5c\u8005\uff1a','').strip() or ''
    i['publishTime'] = len(info)>2 and info[2].split()[0].strip() or str(datetime.date.today())

    source = sel.xpath('//div[@class="text_r"]/div[@class="text_r_b"]/span[1]/text()').extract()
    i['source'] = len(source)>0 and source[0].replace(u'\u6765\u6e90\uff1a','').strip() or ''
    keyWords = sel.xpath('//div[@class="text_r"]/div[@class="text_r_b"]/span[2]/text()').extract()
    i['keyWords'] = len(keyWords)>0 and keyWords[0].replace(u'\u5173\u952e\u5b57\uff1a','').strip().replace(',','|') or ''
    
    content = sel.xpath('//div[@class="textcontent"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'cbinews'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse_articleList(self, response):
    print "enter cbinews_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//ul/li[@class="title"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://www.cbinews.com'+news.xpath('a/@href').extract()[0]
      
      title = news.xpath('a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      i['abstract'] = ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)

  def parse(self, response):
    if 'cloud' in response.url:
      yield FormRequest(url='http://www.cbinews.com/common/page/ArticleList.jsp',formdata={'action':'columnlist','p':'1','pageSize':'45','column_id':'664'},callback=self.parse_articleList)
    if 'bigdata' in response.url:
      yield FormRequest(url='http://www.cbinews.com/common/page/ArticleList.jsp',formdata={'action':'columnlist','p':'1','pageSize':'45','column_id':'666'},callback=self.parse_articleList)
    if 'software' in response.url:
      yield FormRequest(url='http://www.cbinews.com/common/page/ArticleList.jsp',formdata={'action':'columnlist','p':'1','pageSize':'45','column_id':'55'},callback=self.parse_articleList)
