# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

#class InfomationCrawlerPipeline(object):
class BaiduNewsPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['baidu']:
	return item

      conn = pymongo.Connection('localhost',27017)
      infoDB = conn.info
      tArticles = infoDB.articles
      article = {"title":item['title'][0],'sitename':item['sitename'][0],'posttime':item['posttime'][0]}
      tArticles.update({'link':item['href'][0]},{'$set':article},True)

      # print "#"*20
      # print item["title"][0],item['href'][0],item['sitename'][0],item['posttime'][0]

      return item

class StockCompanyInfoPipeline(object):
    def process_item(self, item, spider):
      if spider.name not in ['cninfo']:
	return item

      conn = pymongo.Connection('localhost',27017)
      infoDB = conn.info
      tCompanyInfo = infoDB.stock_companyinfo
      

      company = {
	"stockName":item['stockName'],
	"fullName":item['fullName'],
	"englishName":item['englishName'],
	"regAddress":item['regAddress'],
	"shortName":item['shortName'],
	"legalPerson":item['legalPerson'],
	"secretary":item['secretary'],
	"regCapital":item['regCapital'],
	"industry":item['industry'],
	"postCode":item['postCode'],
	"phone":item['phone'],
	"fax":item['fax'],
	"website":item['website'],
	"listTime":item['listTime'],
	"ipoTime":item['ipoTime'],
	"issueAmount":item['issueAmount'],
	"issuePrice":item['issuePrice'],
	"issuePer":item['issuePer'],
	"issueMode":item['issueMode'],
	"underWriter":item['underWriter'],
	"listSponsor":item['listSponsor'],
	"recomInstitution":item['recomInstitution']
      }
      tCompanyInfo.update({'stockCode':item['stockCode']},{'$set':company},True)

      # print "#"*20
      # print item["stockCode"],item['stockName'],item['regAddress']

      return item
