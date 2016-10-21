import sys
sys.path.append('../../..')

import inspect
from importlib import import_module


spider_module = import_module('spider.spiders.100ec_cn.100ec_cn_news')
for a_spider in [
    cls for name, cls in inspect.getmembers(spider_module, inspect.isclass)
    if cls.__module__ == spider_module.__name__
]:
    print u'{} {}'.format((a_spider.__doc__ , a_spider.name))
