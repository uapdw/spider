from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebActivityItem
from scrapy.http import Request
import datetime
import pymongo
import re

class CsdnActivitySpider(CrawlSpider):
  name = 'csdnActivity'
  allowed_domains = ['csdn.net']
  start_urls = ['http://huiyi.csdn.net/activity/home?&page=1','http://huiyi.csdn.net/activity/home?&page=2','http://huiyi.csdn.net/activity/home?&page=3','http://huiyi.csdn.net/activity/home?&page=4','http://huiyi.csdn.net/activity/home?&page=5']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebActivity = infoDB.web_activity
  
  def parse(self, response):
    print "enter csdnActivity_parse_item...."
    sel = Selector(response)
    items = []
    activityLists = sel.xpath('//div[@class="list-wraper"]/div[@class="item clearfix"]')[0:]
    for activity in activityLists:
      i = WebActivityItem()
      i['url'] = activity.xpath('div[@class="dis"]/dl/dt/a/@href').extract()[0]

      title = activity.xpath('div[@class="dis"]/dl/dt/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''

      trad = activity.xpath('div[@class="dis"]/dl/dd[1]/text()').extract()
      i['trad'] = len(trad)>0 and trad[0].split(u'\uff1a')[1].strip() or ''

      time = activity.xpath('div[@class="dis"]/dl/dd[2]/text()').extract()
      i['time'] = len(time)>0 and time[0].split(u'\uff1a')[1].strip() or ''

      location = activity.xpath('div[@class="dis"]/dl/dd[3]/a/text()').extract()
      i['location'] = len(location)>0 and location[0].strip() or ''

      keyWordList = activity.xpath('div[@class="dis"]/dl/dd[@class="act_tags"]/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords

      activityID = activity.xpath('a/@href').extract()
      i['activityID'] = len(activityID)>0 and activityID[0].split('=')[1] or ''
    
      i['siteName'] = 'csdn'

      i['addTime'] = datetime.datetime.now()
      yield i                                                                               
