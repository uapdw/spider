# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


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
    title = Field()
    author = Field()
    abstract = Field()
    content = Field()
    publish_time = Field()

    source = Field()  # 文章来源
    site_name = Field()

    keywords = Field()

    add_time = Field()
    news_type = Field()
    sentiment = Field()
