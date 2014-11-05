# -*- coding: utf-8 -*-
import datetime
import pymongo
import re
from elasticsearch import Elasticsearch

reComments = re.compile('<!--[^>]*-->')
reHtml = re.compile('</?\w+[^>]*>')
es = Elasticsearch()
conn = pymongo.Connection('localhost',27017)
infoDB = conn.info
tBaiduArticles = infoDB.baidu_articles
tWebArticles = infoDB.web_articles
tWebBlogs = infoDB.web_blogs
tInfReport = infoDB.IndustryReport

es.indices.delete(index='web-articles',ignore=[400,404])

#create indexs
es.indices.create(index="web-articles")

#define mapping
es.indices.put_mapping(
		index="web-articles",
		doc_type="article",
		ignore_conflicts='true',
		body={
			"article":{
				"properties":{
					"sitename":{ "type":"string", "store":"true", "index":"not_analyzed" },
					"addtime":{"type":"date", "store":'true' },
					"publishtime":{"type":"date", "store":'true' },
					"keywords":{"type":"string", "store":'true',"analyzer":"ik" },
					"content":{"type":"string", "store":'true',"analyzer":"ik" },
					"url":{"type":"string", "store":'true', "index":"not_analyzed"},
					"title":{"type":"string","store":'true', "analyzer":"ik"}
					}
				}
			}
		)
es.indices.put_mapping(
		index="web-articles",
		doc_type="baidu",
		ignore_conflicts='true',
		body={
			"baidu":{
				"properties":{
					"sitename":{ "type":"string", "store":"true", "index":"not_analyzed" },
					"addtime":{"type":"date", "store":'true' },
					"publishtime":{"type":"date", "store":'true' },
					"keywords":{"type":"string", "store":'true',"analyzer":"ik" },
					"content":{"type":"string", "store":'true',"analyzer":"ik" },
					"url":{"type":"string", "store":'true', "index":"not_analyzed"},
					"title":{"type":"string","store":'true', "analyzer":"ik"}
					}
				}
			}
		)

es.indices.put_mapping(
		index="web-articles",
		doc_type="report",
		ignore_conflicts='true',
		body={
			"report":{
				"properties":{
					"sitename":{ "type":"string", "store":"true", "index":"not_analyzed" },
					"addtime":{"type":"date", "store":'true' },
					"publishtime":{"type":"date", "store":'true' },
					"infSource":{"type":"string", "store":'true',"index":"not_analyzed" },
					"url":{"type":"string", "store":'true', "index":"not_analyzed"},
					"title":{"type":"string","store":'true', "analyzer":"ik"}
					}
				}
			}
		)
es.indices.put_mapping(
		index="web-articles",
		doc_type="blog",
		ignore_conflicts='true',
		body={
			"blog":{
				"properties":{
					"sitename":{ "type":"string", "store":"true", "index":"not_analyzed" },
					"addtime":{"type":"date", "store":'true' },
					"author":{"type":"string", "store":'true', "index":"not_analyzed" },
					"content":{"type":"string", "store":'true',"analyzer":"ik" },
					"url":{"type":"string", "store":'true', "index":"not_analyzed"},
					"title":{"type":"string","store":'true', "analyzer":"ik"}
					}
				}
			}
		)

'''
listBaiduArticles = tBaiduArticles.find()
for i in listBaiduArticles:
  es.index(index='web-articles',doc_type='baidu', body={'sitename':i['siteName'],'publishtime':i['publishTime'],'url':i['url'],'title':i['title'],'keywords':i['keyWords'],'content':reHtml.sub('',i['content']),'addtime':i['addTime']})
'''
listWebArticles = tWebArticles.find()
for i in listWebArticles:
  if i['publishTime'] == '':
    continue
  print reComments.sub('',reHtml.sub('',i['content']))
  print '='*30
  #es.index(index='web-articles',doc_type='article', body={'sitename':i['siteName'],'addtime':i['addTime'],'publishtime':i['publishTime'],'keywords':i['keyWords'],'url':i['url'],'title':i['title'],'content':reHtml.sub('',i['content'])})

'''
listInfReport = tInfReport.find()
for i in listInfReport:
  es.index(index='web-articles',doc_type='report', body={'sitename':i['siteName'],'addtime':i['addTime'],'publishtime':i['publishTime'],'infsource':i['InfSource'],'url':i['url'],'title':i['title']})

listWebBlogs = tWebBlogs.find()
for i in listWebBlogs:
  es.index(index='web-articles',doc_type='blog',timeout='2m', body={'sitename':i['siteName'],'addtime':i['addTime'],'url':i['url'],'title':i['title'],'content':reHtml.sub('',i['content']),'author':i['author']})
'''
