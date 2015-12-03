# -*- coding: utf-8 -*-

import re
import datetime
from w3lib.html import remove_tags, remove_tags_with_content

# 空白正则表达式
_WHITE_SPACE = re.compile("\s+", re.U)

# html中需要删除的标签
_REMOVE_TAGS = ('script', 'img', 'input')


class XPathExtractor():
    def __init__(self, xpath, join_str=None):
        self.xpath = xpath
        self.join_str = join_str

    def __call__(self, response):
        extract_list = response.selector.xpath(self.xpath).extract()
        if not extract_list or len(extract_list) == 0:
            return ''

        if self.join_str is None:
            return extract_list[0]
        else:
            return self.join_str.join(extract_list)


def text(html_part):
    '''文本extractor
    @type  html_part: unicode
    @param html_part: html的一部分，或者一段文本
    @type  encoding: string
    @param encoding: 编码
    @return: 去掉html标签，压缩连续空白字符为一个空格，的文本
    '''

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

    value = remove_tags_with_content(
        html_part,
        which_ones=_REMOVE_TAGS)

    return value


class DateExtractor():
    def __init__(self, time_format):
        self.time_format = time_format

    def __call__(self, html_part):
        try:
            value = datetime.datetime.strptime(html_part, self.time_format)
            return value
        except:
            return None


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
        i = self.item_class()
        for field, extractors in self.field_extractors_mapping.iteritems():
            value = response
            for extractor in extractors:
                value = extractor(value)
            i[field] = value
        return i
