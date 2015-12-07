# -*- coding: utf-8 -*-

'''补充https://github.com/scrapy/scrapy的loader/processors目录'''

import re
import datetime
import inspect

from dateutil.relativedelta import relativedelta
from w3lib.html import remove_tags, remove_tags_with_content

# 空白正则表达式
_WHITE_SPACE = re.compile("\s+", re.U)

# html中需要删除的标签
_REMOVE_TAGS = ('script', 'img', 'input', 'style')

_MATCHER_TIMEUNIT_MAPPING = {
    re.compile(u'(\d+)秒(以|)前', re.U): 'seconds',
    re.compile(u'(\d+)分(钟|)(以|)前', re.U): 'minutes',
    re.compile(u'(\d+)(小|)时(以|)前', re.U): 'hours',
    re.compile(u'(\d+)(天|日)(以|)前', re.U): 'days',
    re.compile(u'(\d+)(个|)(周|星期|礼拜)(以|)前', re.U): 'weeks',
    re.compile(u'(\d+)(个|)月(以|)前', re.U): 'months',
    re.compile(u'(\d+)年(以|)前', re.U): 'years'
}


class XPathProcessor():
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, response):
        if response is None:
            return None

        return response.selector.xpath(self.xpath).extract()


def text(html_part):
    '''文本extractor
    @type  html_part: unicode
    @param html_part: html的一部分，或者一段文本
    @type  encoding: string
    @param encoding: 编码
    @return: 去掉html标签，压缩连续空白字符为一个空格，的文本
    '''

    if html_part is None:
        return None

    # 去掉html标签
    value = remove_tags(html_part)

    # 压缩连续空白字符为一个空格
    return _WHITE_SPACE.sub(u' ', value).strip()


def safe_html(html_part):
    '''去掉html中一些标签(script、input等)
    @type  html_part: unicode
    @param html_part: html的一部分，或者一段文本
    @type  encoding: string
    @param encoding: 编码
    @return: 去掉html中一些标签的html
    '''

    if html_part is None:
        return None

    value = remove_tags_with_content(
        html_part,
        which_ones=_REMOVE_TAGS)

    return value


class DateProcessor():
    '''日期处理器
    如果匹配给定的format则返回匹配值
    否则按照相对日期（例如：3小时前）匹配
    '''

    def __init__(self, time_format):
        self.time_format = time_format
        self.ago_dict = _MATCHER_TIMEUNIT_MAPPING.copy()

    def __call__(self, datetime_str):
        if datetime_str is None:
            return None

        value = None
        try:
            value = datetime.datetime.strptime(datetime_str, self.time_format)
        except:
            value = self._parse_ago(datetime_str)

        return value

    def _parse_ago(self, datetime_str):
        for matcher, unit in self.ago_dict.iteritems():
            match = matcher.match(datetime_str)
            if match:
                return datetime.datetime.now() + relativedelta(**{
                    unit: -int(match.group(1))
                })


class RegexProcessor():
    '''正则表达式processor
    返回group的list或None
    '''

    def __init__(self, pattern, join_str=u''):
        self.matcher = re.compile(pattern, re.S)
        self.join_str = join_str

    def __call__(self, html_part):
        if html_part is None:
            return None

        result = self.matcher.search(html_part)
        if result:
            return self.join_str.join([g for g in result.groups()])
        else:
            return None


class PipelineProcessor(object):
    '''队列processor
    顺序执行多个processor
    '''

    def __init__(self, *processors):
        self.processors = processors

    def __call__(self, value):
        for processor in self.processors:
            value = processor(value)
        return value


class ItemExtractor(object):
    '''从response中生成item

    field_extractor_mapping，字段和字段extractor列表的映射
    value可以是固定值、函数、callable、函数和callable的混合iterable

    item_class，item的类型
    '''

    def __init__(self, item_class, field_extractor_mapping):
        self.item_class = item_class
        self.field_extractor_mapping = field_extractor_mapping

    def __call__(self, response):
        if response is None:
            return None

        i = self.item_class()
        for field, extractor in self.field_extractor_mapping.iteritems():
            if isinstance(extractor, list):
                value = PipelineProcessor(extractor)(response)
            elif hasattr(extractor, '__call__'):
                value = extractor(response)
            elif inspect.isfunction(extractor):
                value = extractor(response)
            else:
                value = extractor

            i[field] = value
        return i
