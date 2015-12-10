from celery import Celery

app = Celery('spider_task')

app.config_from_object('celeryconfig')

@app.task
def runSpider(spiderName):
  return 'scrapy crawl %s' % spiderName
