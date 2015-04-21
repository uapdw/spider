from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class IresearchNewsSpider(CrawlSpider):
  name = 'iresearchNews'
  allowed_domains = ['iresearch.cn']
  start_urls = ['http://news.iresearch.cn/','http://news.iresearch.cn/lists/oweb/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    title = sel.xpath('//div[@class="content_box"]/h1/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    source = sel.xpath('//div[@class="content_box"]/div[@class="content_titleinfoa"]/span[1]/text()').extract()
    i['source'] = len(source)>0 and source[0].split(u'\uff1a')[1].strip() or ''
    author = sel.xpath('//div[@class="content_box"]/div[@class="content_titleinfoa"]/span[2]/text()').extract()
    i['author'] = len(author)>0 and author[0].split(u'\uff1a')[1].strip() or ''
    pubTime = sel.xpath('//div[@class="content_box"]/div[@class="content_titleinfoa"]/span[3]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split(' ')[0] or str(datetime.date.today())
    keyWords = sel.xpath('//div[@class="content_box"]/div[@class="content_titleinfoa"]/span[4]/a/text()').extract()
    i['keyWords'] = len(keyWords)>0 and keyWords[0].strip() or ''

    abstract = sel.xpath('//div[@class="content_box"]/div[@id="con_div"]/div[@class="review"]/text()').extract()
    i['abstract'] = len(abstract)>0 and abstract[0] or ''

    content = sel.xpath('//div[@class="content_box"]/div[@id="con_div"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'iresearch'
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter iresearch_parse_item...."
    sel = Selector(response)
    items = []
    NewsURL1 = sel.xpath('//ul[@class="new_list"]/li/b/a')[0:]
    NewsURL2 = sel.xpath('//ul[@class="new_list"]/li/p/a')[0:]
    NewsURL3 = sel.xpath('//ul[@class="ul_ellipsis_2 ul_triangle ul_big ie_list_90 bd_1px"][1]/li/a')[0:]
    NewsURL4 = sel.xpath('//ul[@class="ul_ellipsis_2 ul_triangle ul_big ie_list_90 bd_1px"][2]/li/a')[0:]
    NewsURL5 = sel.xpath('//ul[@class="ul_ellipsis_2 ul_triangle ul_big ie_list_90 bd_1px"][3]/li/a')[0:]
    NewsURL = NewsURL1 + NewsURL2 + NewsURL3 + NewsURL4 + NewsURL5
    for news in NewsURL:
      i = WebArticleItem()
      i['url'] = news.xpath('@href').extract()[0]
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
