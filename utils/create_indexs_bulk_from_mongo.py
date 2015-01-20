# -*- coding: utf-8 -*-
import datetime
import pymongo
import re
from elasticsearch import Elasticsearch
from elasticsearch import helpers

print "="*40
print datetime.datetime.now()
print " "

def filter_tags(htmlstr):  
  #先过滤CDATA  
  re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA  
  re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script  
  re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style  
  re_br=re.compile('<br\s*?/?>')#处理换行  
  re_h=re.compile('</?\w+[^>]*>')#HTML标签  
  re_comment=re.compile('<!--[^>]*-->')#HTML注释  
  s=re_cdata.sub('',htmlstr)#去掉CDATA  
  s=re_script.sub('',s) #去掉SCRIPT  
  s=re_style.sub('',s)#去掉style  
  s=re_br.sub('',s)#将br转换为换行  
  s=re_h.sub('',s) #去掉HTML 标签  
  s=re_comment.sub('',s)#去掉HTML注释  
  #去掉多余的空行  
  blank_line=re.compile('\n+')  
  s=blank_line.sub('',s)  
  return s

print "Connect Mongodb...."
reComments = re.compile('<!--[^>]*-->')
reHtml = re.compile('</?\w+[^>]*>')
es = Elasticsearch()
conn = pymongo.Connection('localhost',27017)
infoDB = conn.info
tBaiduArticles = infoDB.baidu_articles
tWebArticles = infoDB.web_articles
tWebBlogs = infoDB.web_blogs
tInfReport = infoDB.IndustryReport
tWeiboContent = infoDB.wb_content
tWeiboUser = infoDB.wb_user
tActivity = infoDB.web_activity

print "Remove index...."
es.indices.delete(index='web-articles',ignore=[400,404])

print "Create index...."
#create indexs
es.indices.create(index="web-articles")

print "Define mapping...."
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
es.indices.put_mapping(
		index="web-articles",
		doc_type="weibo",
		ignore_conflicts='true',
		body={
			"weibo":{
				"properties":{
					"user_id":{ "type":"string", "store":"true"},
					"screen_name":{"type":"string", "store":'true', "index":"not_analyzed" },
					"content":{"type":"string", "store":'true',"analyzer":"ik" },
					"publishtime":{"type":"date", "store":'true' },
					"comments_count":{"type":"integer", "store":'true'},
					"reposts_count":{"type":"integer","store":'true'}
					}
				}
			}
		)
es.indices.put_mapping(
		index="web-articles",
		doc_type="activity",
		ignore_conflicts='true',
		body={
			"activity":{
				"properties":{
					"activityid":{"type":"integer", "store":'true'},
					"addtime":{"type":"date", "store":'true' },
					"keywords":{"type":"string", "store":'true',"analyzer":"ik" },
					"location":{"type":"string", "store":'true',"index":"not_analyzed" },
					"sitename":{ "type":"string", "store":"true","index":"not_analyzed"},
					"time":{ "type":"string", "store":"true","index":"not_analyzed"},
					"title":{"type":"string", "store":'true',"analyzer":"ik" },
					"trad":{ "type":"string", "store":"true","index":"not_analyzed"},
					"url":{ "type":"string", "store":"true","index":"not_analyzed"},
					}
				}
			}
		)


actions = []
'''
print "Create baidu articles indexes...."
listBaiduArticles = tBaiduArticles.find()
for i in listBaiduArticles:
	action = {
		'_index':'web-articles',
		'_type':'baidu',
		'_source':{
			'sitename':i['siteName'],
			'publishtime':i['publishTime'],
			'url':i['url'],
			'title':i['title'],
			'keywords':i['keyWords'],
			'content':filter_tags(i['content']).strip(),
			'addtime':i['addTime']
		}
	}
	actions.append(action)
	if(len(actions) == 500):
		helpers.bulk(es,actions)
		del actions[0:len(actions)]
'''

print "Create other articles indexes...."
listWebArticles = tWebArticles.find()
for i in listWebArticles:
	try:
		if i['publishTime'] == '':
			continue
		action = {
			'_index':'web-articles',
			'_type':'article',
			'_source':{
				'sitename':i['siteName'],
				'addtime':i['addTime'],
				'publishtime':i['publishTime'],
				'keywords':i['keyWords'],
				'url':i['url'],
				'title':i['title'],
				#'content':filter_tags(i['content']).strip()
				'content':''
			}
		}
		actions.append(action)
		if(len(actions) == 500):
			helpers.bulk(es,actions)
			del actions[0:len(actions)]
	except Exception,e:
		print e

print "Create report indexes...."
listInfReport = tInfReport.find()
for i in listInfReport:
	action = {
		'_index':'web-articles',
		'_type':'report',
		'_source':{
			'sitename':i['siteName'],
			'addtime':i['addTime'],
			'publishtime':i['publishTime'],
			'infsource':i['source'],
			'url':i['url'],
			'title':i['title']
		}
	}
	actions.append(action)
	if(len(actions) == 5000):
		helpers.bulk(es,actions)
		del actions[0:len(actions)]

print "Create blog indexes...."
listWebBlogs = tWebBlogs.find()
for i in listWebBlogs:
	action = {
		'_index':'web-articles',
		'_type':'blog',
		'_source':{
			'sitename':i['siteName'],
			'addtime':i['addTime'],
			'url':i['url'],
			'title':i['title'],
			'content':'',
			'author':i['author']
		}
	}
	actions.append(action)
	if(len(actions) == 5000):
		helpers.bulk(es,actions)
		del actions[0:len(actions)]

print "Create weibo indexes...."
listWeiboContent = tWeiboContent.find()
for i in listWeiboContent:
	action = {
		'_index':'web-articles',
		'_type':'weibo',
		'_source':{
			'user_id':i['user_id'],
			'publishtime':i['created_at'],
			'content':i['text'],
			'screen_name':i['screen_name'],
			'comments_count':i['comments_count'],
			'reposts_count':i['reposts_count']
		}
	}
	actions.append(action)
	if(len(actions) == 5000):
		helpers.bulk(es,actions)
		del actions[0:len(actions)]

print "Create activity indexes...."
listActivityContent = tActivity.find()
for i in listActivityContent:
	action = {
		'_index':'web-articles',
		'_type':'activity',
		'_source':{
			'activityid':i['activityID'],
			'addtime':i['addTime'],
			'keywords':i['keyWords'],
			'location':i['location'],
			'sitename':i['siteName'],
			'time':i['time'],
			'title':i['title'],
			'trad':i['trad'],
			'url':i['url']
		}
	}
	actions.append(action)
	if(len(actions) == 5000):
		helpers.bulk(es,actions)
		del actions[0:len(actions)]

if(len(actions) > 0):
	helpers.bulk(es, actions)
	del actions[0:len(actions)]
