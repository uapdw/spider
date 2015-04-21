import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'infomation_crawler.settings') #Must be at the top before other imports
from scrapy import log, signals, project
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue
class CrawlerScript():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)
    def _item_passed(self, item):
        self.items.append(item)
    def _crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.crawler.queue.append_spider(spider)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)
    def crawl(self, spider):
        queue = Queue()
        p = Process(target=self._crawl, args=(queue, spider,))
        p.start()
        p.join()
        return queue.get(True)
# Usage
if __name__ == "__main__":
    log.start()
    """
    This example runs spider1 and then spider2 three times.
    """
    items = list()
    crawler = CrawlerScript()
    items.append(crawler.crawl('spider1'))
    for i in range(3):
        items.append(crawler.crawl('spider2'))
    print items




'''
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
#from infomation_crawler.spiders.followall import FollowAllSpider
from infomation_crawler.spiders.sina import SinaSpider
from scrapy.utils.project import get_project_settings


crawler = Crawler(get_project_settings())
crawler.configure()
spiderList = crawler.spiders.list()
for spiderName in spiderList:
print spiderName


spider = SinaSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()


======================================

class manage:

spiderCounter = 0

def setupCrawler(self, spiderName):
   crawler = Crawler(get_project_settings())
   crawler.signals.connect(self.spiderClosed, signal=signals.spider_closed)
   #crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
   crawler.configure()

   spider = crawler.spiders.create(spiderName)

   crawler.crawl(spider)
   crawler.start()


def spiderClosed(self):
   self.spiderCounter -= 1

   if self.spiderCounter == 0:
       reactor.stop()


def run(self):
   crawler = Crawler(get_project_settings())
   crawler.configure()
   log.start()
   for spiderName in crawler.spiders.list():
       self.spiderCounter += 1
       self.setupCrawler(spiderName)

   reactor.run()


if __name__ == '__main__':
handle = manage()
handle.run()
'''