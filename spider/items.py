# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.exceptions import DropItem


class HBaseItem(Item):

    # hbase 表名
    table_name = None

    # hbase 列族
    column_family = 'column'

    # md5后作为主键的列
    row_key_field = None

    # 必须字段，如果没有值丢弃item
    required_fields = []

    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or not self[required_field]:
                raise DropItem('not field %s' % required_field)


class UradarNewsItem(HBaseItem):

    table_name = 'uradar_news'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'content', 'publish_time']

    url = Field()
    title = Field()
    author = Field()
    abstract = Field()
    content = Field()
    publish_time = Field()
    source = Field()  # 文章来源
    keywords = Field()

    source_domain = Field()
    source_name = Field()

    add_time = Field()
    news_type = Field()
    sentiment = Field()


class UradarBlogItem(HBaseItem):

    table_name = 'uradar_blog'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'content', 'publish_time']

    url = Field()
    title = Field()
    author = Field()
    abstract = Field()
    content = Field()
    publish_time = Field()
    source = Field()
    keywords = Field()

    source_domain = Field()
    source_name = Field()

    add_time = Field()
