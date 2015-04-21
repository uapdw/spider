from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebBlogItem
from scrapy.http import Request
import datetime
import pymongo

class IteyeSpider(CrawlSpider):
  name = 'iteye'
  allowed_domains = ['iteye.com']
  start_urls = ['http://wwwa.iteye.com/blogs', 'http://www.iteye.com/blogs?page=2', 'http://www.iteye.com/blogs?page=3']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebBlogs = infoDB.web_blogs

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']
   
    author = sel.xpath('//div[@id="blog_owner_name"]/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''

    keyWordList = sel.xpath('//div[@class="news_tag"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords

    content = sel.xpath('//div[@id="blog_content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'iteye'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    sel = Selector(response)
    items = []
    indexBlogs = sel.xpath('//div[@id="index_main"]/div[@class="blog clearfix"]')[0:]
    for blog in indexBlogs:
      i = WebBlogItem()
      i['url'] = blog.xpath('div/h3/a/@href').extract()[0]
      
      title = blog.xpath('div/h3/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
    
      abstract = blog.xpath('div/div[1]/text()').extract()
      i['abstract'] = len(abstract)>1 and abstract[1] or ''

      pubTime = blog.xpath('div/div[@class="blog_info"]/span[@class="date"]/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
     
      source = blog.xpath('div/h3/span/a/text()').extract()
      i['source'] = len(source)>0 and source[0][1:-1] or ''    
  
      items.append(i)
    
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
