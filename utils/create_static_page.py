# -*- coding: utf-8 -*-
import re
import os
import datetime
import ssh
from elasticsearch import Elasticsearch

class CreateStaticPage():
	def __init__(self,filePath,fileName):
		self.es = Elasticsearch()
		self.fileName = fileName
		self.filePath = filePath + '/' + fileName
		self.fileServer = '172.16.50.54'
		self.port = 22
		self.userName = 'sftp-daily'
		self.passWord = 'sftp-daily-141216'

	def searchES(self,indexName,typeName,keywords,sizeNum,sortStr):
		self.es = Elasticsearch()
		if typeName == "weibo":
			bodyStr = {
				"query":{
					"match":{
						"content":keywords
					}	
				}		
			}
		else:
			bodyStr = {
				"query":{
					"match":{
						"title":keywords
					}
				}
			}
		res = self.es.search(index=indexName,doc_type=typeName,body=bodyStr,sort=sortStr,size=sizeNum)
		return res
		
	def createPage(self):
    htmlStr = '''
    <style>
body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,select,textarea,button,p,blockquote,table,th,td,menu,figure,img
  {
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Microsoft YaHei', 'Arial Narrow';
}

a {
  text-decoration: none;
}

ul,li {
  list-style: none;
}

.tech-news .fl {
  float: left;
}

.tech-news .fr {
  float: right;
}

.clearfix:before,.clearfix:after {
  content: "";
  display: table;
}

.clearfix:after {
  clear: both;
}

.clearfix {
  zoom: 1;
}

.mt30 {
  margin-top: 30px;
}

.tech-news {
  width: 960px;
  margin: 0 auto;
  /* background:#fafafa; */
}

.one-third {
  width: 34%;
}

.two-third {
  width: 63%;
}

.te-title1 {
  font-size: 21px;
}

.te-title2 {
  font-size: 17px;
  color: #333333;
  font-family: 'Microsoft YaHei', 'Arial Narrow';
  font-weight: bold;
}

.te-font1 {
  font-size: 12px;
  line-height: 30px;
}

.te-black: {
  color: #333333;
}

.tech-news .te-title1 {
  font-weight: bold;
  padding: 15px 0 10px 0;
}

.qutar-block {
  width: 48%;
  float: left;
}

.qutar-block.te-font1 {
  line-height: 26px;
}

.qutar-block .te-title2 {
  margin-top: 20px;
}

.te-dot {
  width: 0px;
  height: 0px;
  border: 2px solid #bbbbbb;
  display: block;
  float: left;
  margin: 12px 7px 0px 0;
}

.te-blog {
  border-bottom: 1px solid #bbbbbb;
  margin-top: 40px;
  padding-bottom: 10px;
}

.te-imgbox {
  width: 90px;
  height: 90px;
  float: left;
  margin: 20px;
}

.blog-list {
  border-bottom: 1px solid #f6f4f4;
}

.blog-list:last-child {
  border-bottom: 1px solid #bbbbbb;
}

span.blog-title a {
  font-weight: bold;
  color: #01638d;
  margin-right: 10px;
}

.blog-list a.link {
  color: #2852ff;
  margin-left: 10px;
}

.blog-list .link-source {
  color: #bdccd5;
}

.qutar-block .te-font1 * {
  vertical-align: middle;
}

.pre-num {
  text-align:center;
  width:16px;
  height:16px; 
  background: #bbbbbb;
  font-size: 10px;
  margin:5px;
  color: #fff;
  line-height:10px;
  padding:4px 1px 0px 1px;
  float:left;
}

.pre-num.hl {
  background: #d71f18;
}

.yy-news div:first-child {
  margin-top: 20px;
}


.yy-news .link-source {
  color: #9c9c9c;
}

.te-font1,.te-font1 a {
  color: #666666;
}

.te-font1 a:hover {
  color: #d71618;
  text-decoration: underline;
}

.te-blog .more {
  font-size: 12px;
  color: #333333;
}

.te-blog .more:hover {
  text-decoration: underline;
  color: #d7df18;
}

.page-support {
  text-align: center;
  color: #828282;
  font-family: SimSum;
  font-size: 12px;
  padding-bottom: 20px;
  width: 75%;
  margin: 90px auto 0 auto;
}

.two-third,.yy-news {
  border-top: 1px solid #bbbbbb;
}

.blog-list .te-font1 {
  margin-top: 12px;
  line-height: 27px;
}

.qutar-block .fir {
  margin-top: 8px;
}

.qutar-block.odd {
  float: right;
}

.qutar-block a {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.yy-news div{
white-space: nowrap;
  overflow:hidden;
}
.yy-news p{
  float:left;
}
.yy-news .link-source{
  float:right;
}
.yy-news .a-wrap{
  width:200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

  <div class="tech-news">
    <div class="te-title1 te-black">
      技术动态
      <div class="one-third fr">用友动态</div>
    </div>
    <div class="clearfix">
      <div class="one-third fr te-font1 yy-news">
    '''

    uapRes = self.searchES('web-articles','article','用友UAP AE 用友BQ UAP UDH 谢东 谢志华',10,'addtime:desc')
    j = 1
    for i in uapRes['hits']['hits']:
      htmlStr += '<div class="clearfix"> '
      if j <= 3:
        className = 'pre-num hl'
      else:
        className = 'pre-num'

      htmlStr += '<p class="'+className+'">'+str(j)+'</p> <p class="a-wrap"><a href="'+(i['_source']['url']).encode('utf8')+'" target=_blank title="'+(i['_source']['title']).encode('utf8')+'">'+(i['_source']['title']).encode('utf8')+'</a> </p> <p class="link-source">['+(i['_source']['sitename']).encode('utf8')+']</p> </div> '
      j += 1
    
    htmlStr += '''
      </div>
      <div class="two-third fl clearfix">
        <div class="qutar-block te-font1">
          <div class="te-title2">大数据</div>
    '''

    bigDataRes = self.searchES('web-articles','article','大数据 Spanner hadoop impala spark storm mahout zookeeper Oozie sqoop flume R语言 HTML5 方法 研究',10,'addtime:desc')
    for i in bigDataRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"> <b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank" title="'+(i['_source']['title']).encode('utf8')+'">'+(i['_source']['title']).encode('utf8')+'</a> </p> '

    htmlStr += '''
        </div>
        <div class="qutar-block te-font1 odd">
          <div class="te-title2">云计算</div>
    '''

    cloudRes = self.searchES('web-articles','article','云计算 方法 研究 算法 混合云',10,'addtime:desc')
    for i in cloudRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank" title="'+(i['_source']['title']).encode('utf8')+'">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
        </div>
        <br style="clear: both;" />
        <div class="qutar-block te-font1">
          <div class="te-title2">移动</div>
    '''

    mobileRes = self.searchES('web-articles','article','移动 移动信息化 移动开发平台 物联网 方法 M2M 企业移动应用平台 企业移动管理 MDM MAM MCM 移动云服务 企业移动应用商店',10,'addtime:desc')
    for i in mobileRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank" title="'+(i['_source']['title']).encode('utf8')+'">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
        </div>
        <div class="qutar-block te-font1 odd">
          <div class="te-title2">安全</div>
    '''

    securityRes = self.searchES('web-articles','article','安全 数据安全 云计算安全 通讯安全 服务器安全 权限 身份管理 设备管理',10,'addtime:desc')
    for i in securityRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank" title="'+(i['_source']['title']).encode('utf8')+'">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
        </div>
      </div>
    </div>
    <div class="te-title1 te-blog">微博</div>
    <ul>
    '''

    weiboRes = self.searchES('web-articles','weibo','HADOOP 开源 JAVA 数据挖掘 商业分析',10,'publishtime:desc')
    for i in weiboRes['hits']['hits']:
      htmlStr +=  '<li class="blog-list clearfix"> <div class="te-imgbox"> <img src="http://udn.yyuap.com/template/yongyou/style/info/person.png" style="width: 90px; height: 90px;" /> </div> <div class="te-font1"> <span class="blog-title"><a href="http://weibo.com/u/'+str(i['_source']['user_id'])+'" target="_blank" title="">'+(i['_source']['screen_name']).encode('utf8')+'</a></span>'+(i['_source']['content']).encode('utf8')+'<br /> <span class="link-source">来自新浪微博</span> </div> </li>'

    htmlStr += '''
    </ul>
    <p class="page-support" title="45456">页面资讯由：用友舆情信息管理系统提供</p>
  </div>
    '''

		self.writeFile(htmlStr)

	def writeFile(self,str):
		print "Write String Into File...."
		fp = open(self.filePath,'w')
		fp.write(str)
		fp.close()

	def uploadFileToUDN(self):
		print "Uploading file to UDN Server...."
		client = ssh.SSHClient()
		client.set_missing_host_key_policy(ssh.AutoAddPolicy())
		client.connect(self.fileServer,self.port,self.userName,self.passWord)

		sftp = client.open_sftp()
		try:
			sftp.put(self.filePath, 'daily/'+self.fileName)
		except Exception,e:
			print e
		


def main():
	csp = CreateStaticPage("/root/sourcecode/information_crawler/web","yuqing.html")
	csp.createPage()
	csp.uploadFileToUDN()

if __name__ == '__main__':
	main()
