# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class InfomationCrawlerPipeline(object):
    def process_item(self, item, spider):
      conn = pymongo.Connection('localhost',27017)
      infoDB = conn.info
      tArticles = infoDB.articles
      article = {"title":item['title'][0],'sitename':item['sitename'][0],'posttime':item['posttime'][0]}
      tArticles.update({'link':item['href'][0]},{'$set':article},True)

      print "#"*20
      print item["title"][0],item['href'][0],item['sitename'][0],item['posttime'][0]

      return item
