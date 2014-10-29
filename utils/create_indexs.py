# -*- coding: utf-8 -*-
import datetime
import pymongo
from elasticsearch import Elasticsearch

es = Elasticsearch()
conn = pymongo.Connection('localhost',27017)
infoDB = conn.info
tBaiduArticles = infoDB.articles
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

listBaiduArticles = tBaiduArticles.find()
for i in listBaiduArticles:
	es.index(index='web-articles',doc_type='article', body={'sitename':i['sitename'],'publishtime':i['publishtime'],'url':i['url'],'title':i['title'],'keywords':i['keywords'],'content':i['content'],'addtime':i['addtime']})

listWebArticles = tWebArticles.find()
for i in listWebArticles:
	if i['publishTime'] == '':
		continue
	es.index(index='web-articles',doc_type='article', body={'sitename':i['siteName'],'addtime':i['addTime'],'publishtime':i['publishTime'],'keywords':i['keyWords'],'url':i['url'],'title':i['title'],'content':i['content']})

listInfReport = tInfReport.find()
for i in listInfReport:
	es.index(index='web-articles',doc_type='report', body={'sitename':i['siteName'],'addtime':i['addTime'],'publishtime':i['publishTime'],'infsource':i['InfSource'],'url':i['url'],'title':i['title']})

listWebBlogs = tWebBlogs.find()
for i in listWebBlogs:
	es.index(index='web-articles',doc_type='blog',timeout='2m', body={'sitename':i['siteName'],'addtime':i['addTime'],'url':i['url'],'title':i['title'],'content':'','author':i['author']})
