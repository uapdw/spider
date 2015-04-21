from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
import re

class CsdnSpider(CrawlSpider):
  name = 'csdn'
  allowed_domains = ['csdn.net']
  start_urls = ['http://www.csdn.net/tag/%E5%A4%A7%E6%95%B0%E6%8D%AE/news', 'http://www.csdn.net/tag/%E5%AE%89%E5%85%A8/news', 'http://www.csdn.net/tag/%E7%A7%BB%E5%8A%A8/news', 'http://www.csdn.net/tag/%E4%BA%91%E8%AE%A1%E7%AE%97/news', 'http://www.csdn.net/tag/%E9%9B%86%E6%88%90/news', 'http://www.csdn.net/tag/%E5%95%86%E4%B8%9A%E5%88%86%E6%9E%90/news', 'http://www.csdn.net/tag/%E5%BC%80%E5%8F%91%E5%B9%B3%E5%8F%B0/news']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
  
  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']
    
    author = sel.xpath('//div[@class="tit_bar"]/span[5]/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''
    
    publishTime = re.findall(r'\d{4}-\d{2}-\d{2}', i['url'], re.M)
    if len(publishTime)>0:
      i['publishTime'] = publishTime[0]
    else:
      i['publishTime'] = str(datetime.date.today())

    content = sel.xpath('//div[@class="con news_content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''
    
    i['siteName'] = 'csdn'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter csdn_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//ul[@class="list"]/li')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('div[@class="line_list"]/a/@href').extract()[0]

      title = news.xpath('div[@class="line_list"]/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''

      abstract = news.xpath('div[@class="line_list"]/span[@class="tag_summary"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''

      source = news.xpath('div[@class="line_list"]/div[@class="dwon_words"]/span[@class="tag_source"][1]/a/text()').extract()
      i['source'] = len(source)>0 and source[0] or ''
      
      keyWordList = news.xpath('div[@class="line_list"]/div[@class="dwon_words"]/span[@class="tag_source"][2]/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
                                                                                      
