# -*- coding: utf-8 -*-
import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re
import datetime
import hashlib
import pymongo

class ESIndexCreator:
	def __init__(self):
		reComments = re.compile('<!--[^>]*-->')
		reHtml = re.compile('</?\w+[^>]*>')

		conn = pymongo.Connection('localhost',27017)
		infoDB = conn.info
		self.tDnsjNews = infoDB.dnsj_news
		self.tDnsjWeibo = infoDB.dnsj_weibo
		self.tDnsjWeixin = infoDB.dnsj_weixin

		self.es = Elasticsearch()

	def __del__(self):
		pass

	def filterTags(self,htmlstr):  
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

	def deleteIndex(self,indexName):
		print "Remove index...."
		self.es.indices.delete(index=indexName,ignore=[400,404])

	def createIndex(self,indexName):
		print "Create index...."
		#create indexs
		self.es.indices.create(index=indexName)

		print "Define mapping...."
		#define mapping
		self.es.indices.put_mapping(
				index=indexName,
				doc_type="article",
				ignore_conflicts='true',
				body={
					"article":{
						"properties":{
							"sitename":{ "type":"string", "store":"true", "index":"not_analyzed" },
							"publishtime":{ "type":"string", "store":"true", "index":"not_analyzed" },
							"url":{"type":"string", "store":'true', "index":"not_analyzed"},
							"title":{"type":"string","store":'true', "analyzer":"ik"}
							}
						}
					}
				)
		self.es.indices.put_mapping(
				index=indexName,
				doc_type="weibo",
				ignore_conflicts='true',
				body={
					"weibo":{
						"properties":{
							"screen_name":{"type":"string", "store":'true', "index":"not_analyzed" },
							"avatarimg":{"type":"string", "store":'true', "index":"not_analyzed" },
							"user_url":{"type":"string", "store":'true', "index":"not_analyzed" },
							"content":{"type":"string", "store":'true',"analyzer":"ik" },
							"publishtime":{"type":"string", "store":'true', "index":"not_analyzed"},
							"weibo_url":{"type":"string", "store":'true', "index":"not_analyzed"},
							}
						}
					}
				)
		self.es.indices.put_mapping(
				index=indexName,
				doc_type="weixin",
				ignore_conflicts='true',
				body={
					"weixin":{
						"properties":{
							"title":{"type":"string", "store":'true',"analyzer":"ik"},
							"content":{"type":"string", "store":'true',"index":"not_analyzed"},
							"publishtime":{"type":"string", "store":'true', "index":"not_analyzed"},
							"url":{"type":"string", "store":'true', "index":"not_analyzed"},
							"imgurl":{"type":"string", "store":'true', "index":"not_analyzed"},
							}
						}
					}
				)


	def createNewsIndex(self,indexName):
		print "Create news index...."
		listNews = self.tDnsjNews.find()
		actions = []
		try:
			for i in listNews:
				action = {
					'_index':indexName,
					'_type':'article',
					'_source':{
						'sitename':i['siteName'],
						'publishtime':i['time'],
						'url':i['url'],
						'title':i['title'],
					}
				}
				actions.append(action)
			helpers.bulk(self.es,actions)
		except Exception,e:
			print e


	def createWeiboIndex(self,indexName):
		print "Create weibo index...."
		listWeibo = self.tDnsjWeibo.find()
		actions = []
		try:
			for i in listWeibo:
				action = {
					'_index':indexName,
					'_type':'weibo',
					'_source':{
						'screen_name':i['username'],
						'avatarimg':i['image'],
						'user_url':i['userurl'],
						'content':i['content'],
						'publishtime':i['time'],
						'weibo_url':i['weibourl']
					}
				}
				actions.append(action)
			helpers.bulk(self.es,actions)
		except Exception,e:
			print e

	def createWeixinIndex(self,indexName):
		print "Create weixin index...."
		listWeixin = self.tDnsjWeixin.find()
		actions = []
		try:
			for i in listWeixin:
				action = {
					'_index':indexName,
					'_type':'weixin',
					'_source':{
						'title':i['title'],
						'content':i['content'],
						'publishtime':i['time'],
						'url':i['url'],
						'imgurl':i['image'],
					}
				}
				actions.append(action)
			helpers.bulk(self.es,actions)
		except Exception,e:
			print e

	def createAllIndex(self,indexName):
		self.deleteIndex(indexName)
		self.createIndex(indexName)
		self.createNewsIndex(indexName)
		self.createWeiboIndex(indexName)
		self.createWeixinIndex(indexName)


def main():
	print "="*40
	print datetime.datetime.now()
	print " "
	
	ic = ESIndexCreator()
	ic.createAllIndex('daniangshuijiao')

if __name__ == "__main__":
	main()


