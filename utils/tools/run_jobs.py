from spider_worker import celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
crawler = CrawlerProcess(settings)

spiderList = crawler.spiders.list()
print len(spiderList)

# for spider in spiderList:
#   print '*'*50
#   print spider
#   print '*'*50
#   celery.runSpider.delay(spider)

# for i in range(50):
#   celery.runSpider.delay('csdn_%s' % i)