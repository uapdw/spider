#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

conn = pymongo.Connection('localhost',27017)
infoDB = conn.info
tKeywords = infoDB.keywords

keywordsList = [
    {'keyword':'大数据','cat':'技术动态','subcat':'大数据'},
    {'keyword':'html5','cat':'技术动态','subcat':'大数据'},
    {'keyword':'hadoop','cat':'技术动态','subcat':'大数据'},
    {'keyword':'云计算','cat':'技术动态','subcat':'云计算'},
    {'keyword':'移动互联','cat':'技术动态','subcat':'移动'},
    {'keyword':'物联网','cat':'技术动态','subcat':'移动'},
    {'keyword':'移动应用','cat':'技术动态','subcat':'移动'},
    {'keyword':'信息安全','cat':'技术动态','subcat':'安全'},
    {'keyword':'SOA','cat':'产品预研','subcat':'企业集成'},
    {'keyword':'BI','cat':'产品预研','subcat':'商业分析'},
    {'keyword':'商业智能','cat':'产品预研','subcat':'商业分析'},
    {'keyword':'SAP','cat':'竞品动态','subcat':'SAP'},
    {'keyword':'oracle','cat':'竞品动态','subcat':'Oracle'},
    {'keyword':'甲骨文','cat':'竞品动态','subcat':'Oracle'},
    {'keyword':'IBM','cat':'竞品动态','subcat':'IBM'},
    {'keyword':'SAS','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'vmware','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'百度','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'普元','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'腾讯','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'腾讯云','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'阿里','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'浪潮','cat':'竞品动态','subcat':'互联网'},
    {'keyword':'Gartner','cat':'研究报告','subcat':'Gartner'},
    {'keyword':'用友UAP','cat':'用友动态','subcat':'用友UAP'},
    {'keyword':'用友','cat':'用友动态','subcat':'用友UAP'},
    {'keyword':'用友NC','cat':'用友动态','subcat':'用友NC'},
    {'keyword':'用友','cat':'用友动态','subcat':'其他'},
    {'keyword':'畅捷通','cat':'用友动态','subcat':'其他'},
    {'keyword':'Java','cat':'技术类自媒体','subcat':'微博'},
    {'keyword':'Hadoop','cat':'技术类自媒体','subcat':'博客'},
    {'keyword':'java','cat':'技术类自媒体','subcat':'博客'},
    {'keyword':'数据挖掘','cat':'技术类自媒体','subcat':'博客'},
    {'keyword':'CIO','cat':'业务拓展','subcat':'CIO'}
]

tKeywords.insert(keywordsList)

a = tKeywords.find()
print a
