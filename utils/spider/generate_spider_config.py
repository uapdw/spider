# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import json

from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

'''配置生成'''


def generate_spider_config():

    settings = get_project_settings()
    spider_loader = SpiderLoader(settings)

    spiders = [
        spider_loader.load(spider_name) for spider_name in spider_loader.list()
    ]

    config = []

    ignore_list = []

    for spider in spiders:
        name = getattr(spider, 'name', '')
        start_urls = getattr(spider, 'start_urls', [])
        allowed_domains = getattr(spider, 'allowed_domains', [])
        target_urls = getattr(spider, 'target_urls', [])
        loader_name = re.sub('Spider', 'Loader', spider.__name__)

        if str(spider.__bases__[0]) != "<class 'spider.spiders.NewsSpider'>" and  str(spider.__bases__[0]) != "<class 'spider.spiders.BlogSpider'>":
            ignore_list.append(name)
            continue

        if len(target_urls) == 0:
            ignore_list.append(name)
            continue

        config.append({
            'start_urls': start_urls,
            'allowed_domains': allowed_domains,
            'target_urls': target_urls,
            'loader_name': loader_name
        })

    print 'ignored spiders: %s' % ignore_list

    f = open('urader_url_config.json', 'w')
    f.write(json.dumps(config))
    f.close()


generate_spider_config()
