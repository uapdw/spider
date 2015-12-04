# -*- coding: utf-8 -*-

from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

from scrapy.item import Item, Field
from spider.extractors import DateExtractor, PipelineExtractor, safe_html


class HBaseItem(Item):

    # hbase 表名
    table_name = None

    # hbase 列族
    column_family = 'column'

    # md5后作为主键的列
    row_key_field = None


class UradarNewsItem(HBaseItem):

    table_name = 'uradar_news'
    row_key_field = 'url'

    url = Field()
    title = Field(input_processor=MapCompose(remove_tags))
    author = Field(input_processor=MapCompose(remove_tags))
    abstract = Field(input_processor=MapCompose(remove_tags))
    content = Field(input_processor=MapCompose(safe_html))
    publish_time = Field()
    source = Field(input_processor=MapCompose(remove_tags))  # 文章来源
    keywords = Field(input_processor=MapCompose(remove_tags))

    source_domain = Field()
    source_name = Field()

    add_time = Field()
    news_type = Field()
    sentiment = Field()
