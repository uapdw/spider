# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import inspect
import re

from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

'''旧爬虫转换'''


def transport_spiders():

    settings = get_project_settings()
    spider_loader = SpiderLoader(settings)

    spiders = [
        spider_loader.load(spider_name) for spider_name in spider_loader.list()
    ]

    start_urls = []
    allowed_domains = []
    source_file = open('source.py', 'w')
    ignore_list = []
    url_loader_dict = {}

    for spider in spiders:
        name = getattr(spider, 'name', '')
        start_urls.extend(getattr(spider, 'start_urls', []))
        allowed_domains.extend(getattr(spider, 'allowed_domains', []))
        target_urls = getattr(spider, 'target_urls', [])

        if str(spider.__bases__[0]) != "<class 'spider.spiders.NewsSpider'>" and  str(spider.__bases__[0]) != "<class 'spider.spiders.BlogSpider'>":
            ignore_list.append(name)
            continue

        if len(target_urls) == 0:
            ignore_list.append(name)
            continue

        for target_url in target_urls:
            url_loader_dict[target_url] = re.sub(
                'Spider', 'Loader', spider.__name__)

        try:
            source = inspect.getsource(spider)
        except:
            ignore_list.append(name)
            continue

        for line in source.split('\n'):
            if re.match('\s*class\s*(\S+)\(\S+\):\s*', line):
                line = re.sub('Spider', 'Loader', line)
            source_file.write(line + '\n')
        source_file.write('\n')

    line = 'from spider.loader.loaders import (\n\t%s\n)\n\n'
    line = re.sub('\t', '    ', line)
    source_file.write(line % ',\n    '.join(
        set([loader for url, loader in url_loader_dict.iteritems()])
    ))
    line = '\tstart_urls = [\n\t\t%s\n\t]\n\n'
    line = re.sub('\t', '    ', line)
    source_file.write(line % ',\n        '.join(
        ["'" + url + "'" for url in start_urls]
    ))
    line = '\tallowed_domains = [\n\t\t%s\n\t]\n\n'
    line = re.sub('\t', '    ', line)
    source_file.write(line % ',\n        '.join(
        ["'" + domain + "'" for domain in allowed_domains]
    ))
    line = '\tmatcher_loader_dict = {\n\t\t%s\n\t}\n\n'
    line = re.sub('\t', '    ', line)
    source_file.write(line % ',\n        '.join(
        ["re.compile('%s'): %s()" % (url, loader) for url, loader in url_loader_dict.iteritems()]
    ))

    source_file.flush()
    source_file.close()

    print 'ignored spiders: %s' % ignore_list

transport_spiders()
