# -*- coding: utf-8 -*-

import datetime

from scrapy.loader.processors import TakeFirst, MapCompose, Join

from spider.loader import ItemLoader
from spider.loader.processors import (SafeHtml, text, DateProcessor,
                                      RegexProcessor, PipelineProcessor)
from spider.items import UradarNewsItem, UradarBlogItem, HBaseItem


class MergeLoader(object):

    def __init__(self, loader_list):
        self.loader_list = loader_list

    def load(self, response):
        for loader in self.loader_list:
            try:
                i = loader.load(response)

                if isinstance(i, HBaseItem):
                    i.validate()

                if i is not None:
                    return i
            except:
                continue


class NewsLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'content_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    title_xpath = '//title'
    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarNewsItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)), Join('\n'))

        # author可选
        auther_xpath = getattr(self, 'author_xpath', None)
        if auther_xpath is not None:
            auther_re = getattr(self, 'author_re', None)
            if auther_re is None:
                l.add_xpath('author', self.author_xpath, MapCompose(text))
            else:
                l.add_xpath('author', self.author_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选

        processor_list = [text]

        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is not None:
            processor_list.append(
                RegexProcessor(
                    publish_time_re,
                    join_str=getattr(self, 'publish_time_re_join', u'')
                )
            )

        publish_time_filter = getattr(self, 'publish_time_filter', None)
        if publish_time_filter is not None:
            processor_list.append(
                publish_time_filter
            )

        processor_list.append(DateProcessor(self.publish_time_format))

        l.add_xpath('publish_time', self.publish_time_xpath,
                    MapCompose(
                        PipelineProcessor(
                            *processor_list
                        )
                    ))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source可选
        source_xpath = getattr(self, 'source_xpath', None)
        if source_xpath:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()

        return i


class BlogLoader(object):
    '''新闻爬虫'''

    subclass_required_attrs = [
        'title_xpath',
        'content_xpath',
        'author_xpath',
        'publish_time_xpath',
        'publish_time_format'
    ]

    abstract_xpath = '//meta[@name="description"]/@content'
    keywords_xpath = '//meta[@name="keywords"]/@content'

    def __init__(self):
        for attr in self.subclass_required_attrs:
            if not getattr(self, attr, None):
                raise ValueError(
                    "%s must have a %s" % (type(self).__name__, attr)
                )

        if not getattr(self, 'site_domain', None) and \
                not getattr(self, 'source_domain', None):
            raise ValueError(
                "%s must have a site_domain" % (type(self).__name__, attr)
            )

        if not getattr(self, 'site_name', None) and \
                not getattr(self, 'source_name', None):
            raise ValueError(
                "%s must have a site_name" % (type(self).__name__, attr)
            )

    def load(self, response):
        l = ItemLoader(item=UradarBlogItem(), response=response)

        l.default_output_processor = TakeFirst()

        l.add_value('url', response.url)

        l.add_xpath('title', self.title_xpath, MapCompose(text))

        l.add_xpath('content', self.content_xpath,
                    MapCompose(SafeHtml(response.url)))

        # author_re可选
        auther_re = getattr(self, 'author_re', None)
        if auther_re is None:
            l.add_xpath('author', self.author_xpath, MapCompose(text))
        else:
            l.add_xpath('author', self.author_xpath, MapCompose(text),
                        MapCompose(RegexProcessor(auther_re)))

        # publish_time_re可选
        publish_time_re = getattr(self, 'publish_time_re', None)
        if publish_time_re is None:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   DateProcessor(self.publish_time_format))))
        else:
            l.add_xpath('publish_time', self.publish_time_xpath,
                        MapCompose(PipelineProcessor(
                                   text,
                                   RegexProcessor(publish_time_re),
                                   DateProcessor(self.publish_time_format))))

        # abstract默认使用meta中description
        l.add_xpath('abstract', self.abstract_xpath, MapCompose(text))

        # keywords默认使用meta中keywords
        l.add_xpath('keywords', self.keywords_xpath, MapCompose(text))

        # source_re可选
        if getattr(self, 'source_xpath', None) is not None:
            source_re = getattr(self, 'source_re', None)
            if source_re is None:
                l.add_xpath('source', self.source_xpath, MapCompose(text))
            else:
                l.add_xpath('source', self.source_xpath, MapCompose(text),
                            MapCompose(RegexProcessor(source_re)))

        l.add_value('site_domain', getattr(self, 'site_domain', None))
        l.add_value('site_name', getattr(self, 'site_name', None))

        # 兼容原有爬虫
        l.add_value('site_domain', getattr(self, 'source_domain', None))
        l.add_value('site_name', getattr(self, 'source_name', None))

        l.add_value('add_time', datetime.datetime.now())

        i = l.load_item()
        return i


from spider.loader.loaders.it168_com.it168_com_news import It168NewsLoader
from spider.loader.loaders.data_tsci_com_cn.data_tsci_com_cn_news import DataTsciComCnNewsLoader
from spider.loader.loaders.qudong_com.qudong_com_news import QudongNewsLoader
from spider.loader.loaders.kn58_com.kn58_com_news import Kn58NewsLoader
from spider.loader.loaders.csdn_net.csdn_net_news import CSDNNewsLoader
from spider.loader.loaders.csdn_net.csdn_net_blog import CSDNBlogLoader
from spider.loader.loaders.techweb_com_cn.techweb_com_cn_news import TechwebNewsLoader
from spider.loader.loaders.cnsoftnews_com.cnsoftnews_com_news import CnsoftNewsLoader
from spider.loader.loaders.ctocio_com.ctocio_com_news import CtocioNewsLoader
from spider.loader.loaders.n199it_com.n199it_com_news import N199itNewsLoader
from spider.loader.loaders.qq_com.qq_com_news import QQNewsLoader
from spider.loader.loaders.cnii_com_cn.cnii_com_cn_news import CniiComCnNewsLoader
from spider.loader.loaders.leiphone_com.leiphone_com_news import LeiphoneNewsLoader
from spider.loader.loaders.zol_com_cn.zol_com_cn_news import ZolNewsLoader
from spider.loader.loaders.e_works_net_cn.eworks_net_cn_news import EworksNewsLoader
from spider.loader.loaders.sootoo_com.sootoo_com_news import SootooNewsLoader
from spider.loader.loaders.vsharing_com.vsharing_com_news import VsharingNewsLoader
from spider.loader.loaders.people_com_cn.people_com_cn_news import PeopleComCnNewsLoader
from spider.loader.loaders.n163_com.n163_com_news import WWW163NewsLoader
from spider.loader.loaders.zjol_com_cn.zjol_com_cn_news import ZJOLComCnNewsLoader
from spider.loader.loaders.idc_com_cn.idc_com_cn_news import IdcNewsLoader
from spider.loader.loaders.eastday_com.eastday_com_news import EastDayNewsLoader
from spider.loader.loaders.caijing_com_cn.caijing_com_cn_news import CaijingNewsLoader
from spider.loader.loaders.ccidnet_com.ccidnet_com_news import CcidnetNewsLoader
from spider.loader.loaders.chinabyte_com.chinabyte_com_news import ChinabyteNewsLoader
from spider.loader.loaders.ciotimes_com.ciotimes_com_news import CiotimesNewsLoader
from spider.loader.loaders.xinhuanet_com.xinhuanet_com_news import XinhuanetNewsLoader
from spider.loader.loaders.china_com_cn.china_com_cn_news import ChinaComCnNewsLoader
from spider.loader.loaders.pcpop_com.pcpop_com_news import PcpopNewsLoader
from spider.loader.loaders.sap_com.sap_com_news import SapNewsLoader
from spider.loader.loaders.spn_com_cn.spn_com_cn_news import SPNComNewsLoader
from spider.loader.loaders.enorth_com_cn.enorth_com_cn_news import ENorthNewsLoader
from spider.loader.loaders.n100ec_cn.n100ec_cn_news import N100ecNewsLoader
from spider.loader.loaders.cbinews_com.cbinews_com_news import CbinewsNewsLoader
from spider.loader.loaders.n36dsj_com.n36dsj_com_news import N36dsjNewsLoader
from spider.loader.loaders.sina_com_cn.sina_com_cn_news import SinaNewsLoader
from spider.loader.loaders.ycwb_com.ycwb_com_news import YCWBNewsLoader
from spider.loader.loaders.cbismb_com.cbismb_com_news import CbismbNewsLoader
from spider.loader.loaders.gmw_cn.gmw_cn_news import GmwNewsLoader
from spider.loader.loaders.sohu_com.sohu_com_news import SohuNewsLoader
from spider.loader.loaders.china_com.china_com_news import ChinaNewsLoader
from spider.loader.loaders.ccw_com_cn.ccw_com_cn_news import CcwNewsLoader
from spider.loader.loaders.cqnews_net.cqnews_net_news import CqNewsNetNewsLoader
from spider.loader.loaders.china_cloud_com.china_cloud_com_news import ChinaCloudNewsLoader
from spider.loader.loaders.yidonghua_com.yidonghua_com_news import YidonghuaNewsLoader
from spider.loader.loaders.dataguru_cn.dataguru_cn_news import DataguruNewsLoader
from spider.loader.loaders.s3d4_cn.s3d4_cn_news import S3d4NewsLoader
from spider.loader.loaders.topoint_com_cn.topoint_com_cn_news import TopointNewsLoader
from spider.loader.loaders.cctime_com.cctime_com_news import CctimeNewsLoader
from spider.loader.loaders.zdnet_com_cn.zdnet_com_cn_news import ZdnetNewsLoader
from spider.loader.loaders.ynet_com.ynet_com_news import YnetNewsLoader
from spider.loader.loaders.hexun_com.hexun_com_news import HexunNewsLoader
from spider.loader.loaders.yesky_com.yesky_com_news import YeskyComNewsLoader
from spider.loader.loaders.qianlong_com.qianlong_com_news import QianLongNewsLoader
from spider.loader.loaders.ifeng_com.ifeng_com_news import IFengNewsLoader
from spider.loader.loaders.ceocio_com_cn.ceocio_com_cn_news import CeocioNewsLoader
from spider.loader.loaders.autohome_com_cn.autohome_com_cn_bbs import AutohomeComCnBBSLoader
from spider.loader.loaders.xcar_com_cn.xcar_com_cn_bbs import XcarComCnBBSLoader
from spider.loader.loaders.sina_com_cn.sina_com_cn_bbs import SinaComCnBBSLoader
from spider.loader.loaders.ganzhou_gov_cn.ganzhou_gov_cn_news import GanZhouNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzhrss_gov_cn_news import GZHrssNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzsczj_gov_cn_news import GZSCZJNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzstc_gov_cn_news import GZStcNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzciit_gov_cn_news import GZCiitNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzsdpc_gov_cn_news import GZSdpcNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gz315_gov_cn_news import GZ315NewsLoader
from spider.loader.loaders.ganzhou_gov_cn.sipo_gov_cn_news import SiPoNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzdofcom_gov_cn_news import GZDoFComNewsLoader
from spider.loader.loaders.ganzhou_gov_cn.gzsl_gov_cn_news import GZSLNewsLoader
__all__ = [
    'It168NewsLoader',
    'DataTsciComCnNewsLoader',
    'QudongNewsLoader',
    'Kn58NewsLoader',
    'CSDNNewsLoader',
    'CSDNBlogLoader',
    'TechwebNewsLoader',
    'CnsoftNewsLoader',
    'CtocioNewsLoader',
    'N199itNewsLoader',
    'QQNewsLoader',
    'CniiComCnNewsLoader',
    'LeiphoneNewsLoader',
    'ZolNewsLoader',
    'EworksNewsLoader',
    'SootooNewsLoader',
    'VsharingNewsLoader',
    'PeopleComCnNewsLoader',
    'WWW163NewsLoader',
    'ZJOLComCnNewsLoader',
    'IdcNewsLoader',
    'EastDayNewsLoader',
    'CaijingNewsLoader',
    'CcidnetNewsLoader',
    'ChinabyteNewsLoader',
    'CiotimesNewsLoader',
    'XinhuanetNewsLoader',
    'ChinaComCnNewsLoader',
    'PcpopNewsLoader',
    'SapNewsLoader',
    'SPNComNewsLoader',
    'ENorthNewsLoader',
    'N100ecNewsLoader',
    'CbinewsNewsLoader',
    'N36dsjNewsLoader',
    'SinaNewsLoader',
    'YCWBNewsLoader',
    'CbismbNewsLoader',
    'GmwNewsLoader',
    'SohuNewsLoader',
    'ChinaNewsLoader',
    'CcwNewsLoader',
    'CqNewsNetNewsLoader',
    'ChinaCloudNewsLoader',
    'YidonghuaNewsLoader',
    'DataguruNewsLoader',
    'S3d4NewsLoader',
    'TopointNewsLoader',
    'CctimeNewsLoader',
    'ZdnetNewsLoader',
    'YnetNewsLoader',
    'HexunNewsLoader',
    'YeskyComNewsLoader',
    'QianLongNewsLoader',
    'IFengNewsLoader',
    'CeocioNewsLoader',
    'AutohomeComCnBBSLoader',
    'XcarComCnBBSLoader',
    'SinaComCnBBSLoader',
    'GanZhouNewsLoader',
    'GZHrssNewsLoader',
    'GZStcNewsLoader',
    'GZSCZJNewsLoader',
    'GZCiitNewsLoader',
    'GZSdpcNewsLoader',
    'GZ315NewsLoader',
    'SiPoNewsLoader',
    'GZDoFComNewsLoader',
    'GZSLNewsLoader'
]
