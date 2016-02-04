# -*- coding: utf-8 -*-

import datetime

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

        publish_time = getattr(self, 'publish_time', None)
        if isinstance(publish_time, datetime.datetime) and \
                publish_time > datetime.datetime.now():
            raise DropItem('invalid publish_time %s' % publish_time)

    def get_row_key(self):
        return self[self.row_key_field]


class UradarWeiboItem(HBaseItem):
    table_name = 'uradar_weibo'

    required_fields = ['weibo_id', 'weibo_url', 'content', 'created_at']

    weibo_id = Field()
    weibo_url = Field()
    content = Field()
    created_at = Field()

    user_url = Field()
    screen_name = Field()
    user_pic = Field()

    comment_count = Field()
    repost_count = Field()

    def get_row_key(self):
        return self['weibo_url']


class UradarBBSItem(HBaseItem):
    table_name = 'uradar_bbs'
    required_fields = ['thread_id', 'post_id', 'url', 'title', 'content',
                       'publish_time']

    thread_id = Field()
    post_id = Field()

    url = Field()
    title = Field()
    abstract = Field()
    keywords = Field()
    content = Field()
    author = Field()
    publish_time = Field()

    source = Field()

    site_domain = Field()
    site_name = Field()

    sentiment = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (self['site_domain'], self['thread_id'],
                             self['post_id'])


class UradarArticleItem(HBaseItem):

    table_name = 'uradar_article'
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

    article_type = Field()  # 文章类型
    site_domain = Field()
    site_name = Field()

    add_time = Field()
    sentiment = Field()


class UradarNewsItem(UradarArticleItem):

    def __init__(self):
        super(UradarNewsItem, self).__init__(article_type='1')


class UradarBlogItem(UradarArticleItem):

    def __init__(self):
        super(UradarBlogItem, self).__init__(article_type='3')


class UradarWeixinItem(UradarArticleItem):

    def __init__(self):
        super(UradarWeixinItem, self).__init__(article_type='2')


class UradarReportItem(UradarArticleItem):

    def __init__(self):
        super(UradarReportItem, self).__init__(article_type='4')


class UradarActivityItem(HBaseItem):

    table_name = 'uradar_activity'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'start_time', 'end_time']

    url = Field()
    title = Field()
    start_time = Field()
    end_time = Field()
    location = Field()
    trad = Field()
    content = Field()
    keywords = Field()

    source_domain = Field()
    source_name = Field()
    add_time = Field()
