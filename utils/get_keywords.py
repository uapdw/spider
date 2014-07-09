#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

conn = pymongo.Connection('localhost',27017)
infoDB = conn.info
tKeywords = infoDB.keywords

arrKeywords = tKeywords.find()
for i in arrKeywords:
  print i['keyword']
