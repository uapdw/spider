# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import inspect
import re
import os

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
    ignore_list = []
    url_loader_dict = {}

    import_list = []

    # 创建loaders目录
    if not os.path.exists('g_loaders'):
        os.mkdir('g_loaders')

    for spider in spiders:
        name = getattr(spider, 'name', '')
        start_urls.extend(getattr(spider, 'start_urls', []))
        allowed_domains.extend(getattr(spider, 'allowed_domains', []))
        target_urls = getattr(spider, 'target_urls', [])

        parent_class = None
        if str(spider.__bases__[0]) == "<class 'spider.spiders.NewsSpider'>":
            parent_class = 'NewsLoader'
        elif str(spider.__bases__[0]) == "<class 'spider.spiders.BlogSpider'>":
            parent_class = 'BlogLoader'

        if parent_class is None:
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

        # 爬虫文件所在目录名
        parent_package = spider.__module__.split('.')[-2]

        import_list.append(
            {
                'path': parent_package,
                'file': name,
                'class': re.sub('Spider', 'Loader', spider.__name__)
            }
        )

        loader_path = 'g_loaders/%s' % parent_package
        if not os.path.exists(loader_path):
            os.mkdir(loader_path)
            open('%s/__init__.py' % loader_path, 'w').close()

        loader_file = open('%s/%s.py' % (loader_path, name), 'w')
        loader_file.write('# -*- coding: utf-8 -*-\n\n')
        loader_file.write(
            'from spider.loader.loaders import %s\n\n\n' % parent_class
        )

        lines = source.split('\n')
        for index, line in enumerate(lines):
            if re.match('\s*class\s*(\S+)\(\S+\):\s*', line):
                line = re.sub('Spider', 'Loader', line)
            if index != len(lines) - 1:
                loader_file.write(line + '\n')
        loader_file.flush()
        loader_file.close()

    # loaders目录init文件
    init_file = open('g_loaders/__init__.py', 'w')
    init_file.write('# -*- coding: utf-8 -*-\n\n')
    for item in import_list:
        init_file.write('from spider.loader.loaders.%s.%s import %s\n' % (
            item['path'],
            item['file'],
            item['class']
        ))
    init_file.write("\n__all__ = [\n\t%s\n]" % ',\n\t'.join(
        ["'%s'" % item['class'] for item in import_list]
    ))
    init_file.flush()
    init_file.close()

    # 写入uradar_url.py文件中的内容
    source_file = open('g_uradar_url.py', 'w')

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
