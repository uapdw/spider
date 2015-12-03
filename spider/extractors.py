# -*- coding: utf-8 -*-

import re
import datetime
from dateutil.relativedelta import relativedelta
from w3lib.html import remove_tags, remove_tags_with_content

# 空白正则表达式
_WHITE_SPACE = re.compile("\s+", re.U)

# html中需要删除的标签
_REMOVE_TAGS = ('script', 'img', 'input')

_MATCHER_TIMEUNIT_MAPPING = {
    re.compile(u'(\d+)秒(以|)前', re.U): 'seconds',
    re.compile(u'(\d+)分(钟|)(以|)前', re.U): 'minutes',
    re.compile(u'(\d+)(小|)时(以|)前', re.U): 'hours',
    re.compile(u'(\d+)(天|日)(以|)前', re.U): 'days',
    re.compile(u'(\d+)(个|)(周|星期|礼拜)(以|)前', re.U): 'weeks',
    re.compile(u'(\d+)(个|)月(以|)前', re.U): 'months',
    re.compile(u'(\d+)年(以|)前', re.U): 'years'
}


class XPathExtractor():
    def __init__(self, xpath, join_str=None):
        self.xpath = xpath
        self.join_str = join_str

    def __call__(self, response):
        if response is None:
            return None

        extract_list = response.selector.xpath(self.xpath).extract()
        if not extract_list or len(extract_list) == 0:
            return ''

        if self.join_str is None:
            return extract_list[0]
        else:
            return self.join_str.join(extract_list)


def now(response):
    '''现在，用于生成addtime'''
    return datetime.datetime.now()


class FixValueExtractor():
    '''固定值，用于source_name、source_domain等固定值'''

    def __init__(self, fix_value):
        self.fix_value = fix_value

    def __call__(self, response):
        return self.fix_value


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


class DateExtractor():
    '''日期读取器
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
            pass

        if value is None:
            value = self.__parse_ago(datetime_str)

        return value

    def __parse_ago(self, datetime_str):
        for matcher, unit in self.ago_dict.iteritems():
            match = matcher.match(datetime_str)
            if match:
                return datetime.datetime.now() + relativedelta(**{
                    unit: match.group(1)
                })


class RegexExtractor():
    def __init__(self, pattern):
        self.matcher = re.compile(pattern, re.S)

    def __call__(self, html_part):
        if html_part is None:
            return None

        result = self.matcher.search(html_part)
        if result:
            return u''.join(
                [g for g in result.groups() or result.group() if result]
            )


class ItemExtractor(object):
    '''从response中生成item
    field_extractors_mapping，字段和字段extractor列表的映射
    item_class，item的类型
    新建item_class实例，遍历field_extractors_mapping中映射，顺序执行extractor生成字段值
    '''

    def __init__(self):
        if not getattr(self, 'field_extractors_mapping', None):
            raise ValueError(
                "%s must have a field_extractors_mapping" % type(self).__name__
            )
        if not getattr(self, 'item_class', None):
            raise ValueError(
                "%s must have a nonempty item_class" % type(self).__name__
            )

    def __call__(self, response):
        if response is None:
            return None

        i = self.item_class()
        for field, extractors in self.field_extractors_mapping.iteritems():
            value = response
            for extractor in extractors:
                value = extractor(value)
            i[field] = value
        return i
