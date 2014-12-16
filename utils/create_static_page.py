# -*- coding: utf-8 -*-
import re
import os
import datetime
from elasticsearch import Elasticsearch

class CreateStaticPage():
	def __init__(self,filePath,fileName):
		self.es = Elasticsearch()
		self.filePath = filePath + '/' + fileName

	def searchES(self,indexName,typeName,keywords,sizeNum,sortStr):
		self.es = Elasticsearch()
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
		'''
		print res
		for i in res['hits']['hits']:
			print i["_source"]['title']
			print i["_source"]['addtime']
		'''

		htmlStr = '''
		<!DOCTYPE html>
<html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <style>
  body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,select,textarea,button,p,blockquote,table,th,td,menu,figure,img
  { 
    margin: 0;
    padding: 0;
  }
  body{
    font-family: 'Microsoft YaHei', 'Arial Narrow';
  }
  a{
    text-decoration:none;
  }
  ul,li{
    list-style:none;
  }
  .fl{
    float:left;
  } 
  .fr{
    float:right;
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
  .mt30{
    margin-top:30px;
  }
  
  .tech-news{
    width:960px;
    margin: 0 auto;
    /* background:#fafafa; */
  }
  
  .one-third{
    width:34%;
  }
  .two-third{
    width:63%;  
  }
  
  .te-title1{
    font-size:21px;
  }
  .te-title2{
    font-size:17px;
    color:#333333;
    font-family: 'Microsoft YaHei', 'Arial Narrow';
    font-weight:bold;
  }
  .te-font1{
    font-size:12px;
    line-height:30px;
  }
  
  .te-black:{
    color:#333333;
  }
  .tech-news .te-title1{
    font-weight:bold;
    padding:15px 0 10px 0;
  }
  .qutar-block{
    width:50%;
    float:left;
  }
  .qutar-block.te-font1{
    line-height:26px;
  }
  .qutar-block .te-title2{
    margin-top:20px;
  }
  .te-dot{
    width:0px;
    height:0px;
    border:2px solid #bbbbbb;
    display:block;
    float:left;
    margin: 12px 7px 0px 0;
  }
  .te-blog{
    border-bottom:1px solid #bbbbbb;
    margin-top:40px;
    padding-bottom:10px;
  }
  .te-imgbox{
    width:90px;
    height:90px;
    float:left;
    margin:20px;
  }
  .blog-list{
    border-bottom:1px solid #bbbbbb;
  }
  .blog-title{
    font-weight:bold;
    color:#01638d;
    margin-right:10px;
  }
  .blog-list a.link{
    color:#2852ff;
    margin-left:10px;
  }
  .blog-list .link-source{
    color:#bdccd5;
  }
  .qutar-block .te-font1 *{
    vertical-align:middle;
  }
  .pre-num{
    padding:0px 2px;
    background:#bbbbbb;
    font-size:10px;
    margin-right:5px;
    color:#fff;
  }
  .pre-num.hl{
    background:#d71f18;
  }
  .yy-news p:first-child{
    margin-top:20px;  
  }
  .yy-news .link-source{
    float:right;
    color:#9c9c9c;
  }
  .te-font1,.te-font1 a{
    color:#666666;
  }
  .te-font1 a:hover{
    color:#d71618;
    text-decoration:underline;
  }
  .te-blog .more{
    font-size:12px;
    color:#333333;
  }
  .te-blog .more:hover{
    text-decoration:underline;
    color:#d7df18;
  }
  .page-support{
    text-align:center;
    color:#828282;
    font-family:SimSum;
    font-size:12px;
    padding-bottom:20px;
    border-bottom:1px solid #bbbbbb;
    width:75%;
    margin:90px auto 0 auto ;
  }
  .two-third,.yy-news{
    border-top:1px solid #bbbbbb;
  }
  .blog-list .te-font1{
    margin-top:12px;
    line-height:27px;
  }
  .qutar-block .fir{
    margin-top:8px;
  }
  .qutar-block.odd{
    float:right;
  }
  </style>
  </head>
  <body>
    <div class="tech-news">
      <div class="te-title1 te-black">
        技术动态
        <div class="one-third fr">用友动态</div>
      </div>
      <div class="clearfix">
        <div class="one-third fr te-font1 yy-news">
        '''

    uapRes = self.searchES('web-articles','article','用友UAP AE 用友BQ UAP UDH 谢东 谢志华',20,'addtime:desc')
    j = 1
    for i in uapRes['hits']['hits']:
      htmlStr +=  '<p><b class="pre-num hl">'+j+'</b><a href="'+(i['_source']['url']).encode('utf8')+'" target=_blank>'+(i['_source']['title']).encode('utf8')+'</a><span class="link-source">['+(i['_source']['sitename']).encode('utf8')+']</span></p>'
      j++


    htmlStr += '''
        </div>
        <div class="two-third fl clearfix">
          <div class="qutar-block te-font1">
            <div class="te-title2">大数据</div>
            '''

    bigDataRes = self.searchES('web-articles','article','大数据 Spanner hadoop impala spark storm mahout zookeeper Oozie sqoop flume R语言 HTML5 方法 研究',20,'addtime:desc')
    for i in bigDataRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
          </div>
          <div class="qutar-block te-font1 odd">
            <div class="te-title2">云计算</div>
            '''

    cloudRes = self.searchES('web-articles','article','云计算 方法 研究 算法 混合云',20,'addtime:desc')
    for i in cloudRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
          </div>
          <br style="clear:both;"/>
          <div class="qutar-block te-font1">
            <div class="te-title2">移动</div>
            '''

    mobileRes = self.searchES('web-articles','article','移动 移动信息化 移动开发平台 物联网 方法 M2M 企业移动应用平台 企业移动管理 MDM MAM MCM 移动云服务 企业移动应用商店',20,'addtime:desc')
    for i in mobileRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
          </div>
          <div class="qutar-block te-font1 odd">
            <div class="te-title2">安全</div>
            '''

    securityRes = self.searchES('web-articles','article','安全 数据安全 云计算安全 通讯安全 服务器安全 权限 身份管理 设备管理',20,'addtime:desc')
    for i in securityRes['hits']['hits']:
      htmlStr +=  '<p class="clearfix fir"><b class="te-dot"></b><a href="'+(i['_source']['url']).encode('utf8')+'" target="_blank">'+(i['_source']['title']).encode('utf8')+'</a></p>'

    htmlStr += '''
          </div>
        </div>
      </div>
      <div class="te-title1 te-blog">
        微博
      </div>
      <ul>
      '''
    weiboRes = self.searchES('web-articles','article','HADOOP 开源 JAVA 数据挖掘 商业分析',20,'addtime:desc')
    for i in weiboRes['hits']['hits']:
      htmlStr +=  '<li class="blog-list clearfix"> <div class="te-imgbox"><img src="./person.png"/></div> <div class="te-font1"> <span class="blog-title">'+(i['_source']['screen_name']).encode('utf8')+'</span>'+(i['_source']['content']).encode('utf8')+'<br/><span class="link-source"><a href="http://weibo.com/u/'+i['_source']['user_id']+'" target="_blank">来自新浪微博</a></span> </div> </li> '
    
    htmlStr += '''
      </ul>
      <p class="page-support">页面资讯由：用友舆情信息管理系统提供</p>
    </div>
  </body>
</html>
		'''

		
		htmlStr += '''
									</ul>

							 </div>
						</div>
			 </div>
			 
			 <!-- 移动专区静态展示 -->
			 <!--
			 <div class="line clearfix">
						 <div class="l ltext part">
							<p class="ttitle zero">简单&nbsp;快速&nbsp;高效</p>
								<div class="ccontent">
								<span>通过用友移动开发平台可以开发出完全媲美原生应用的App一次开发，多平台、多分辨率，多机型，自动全适配。</span>            <p class="clearfix down">
								<a href="/forum.php?mod=viewthread&amp;tid=8142" class="load plugin" target="_blank"></a>
								<a href="/forum.php?mod=viewthread&amp;tid=8165" class="load file" target="_blank"></a>
								<a href="/forum.php?mod=viewthread&amp;tid=8164" class="load train" target="_blank"></a>
								</p>
								</div>
								
						 </div>
						 <div class="r rimage part zero">
						 </div>
			 </div>
			 -->
			 
		</div>
		</div>

		<div>
		<div class="footer">
		<div id="ft" class="wp" style="margin: 0 auto; position: relative; border-radius: 0; border-top: 2px solid #e8e8e8;">
		<div style="text-align: center;">
		<span>
		<a href="http://www.yonyou.com">用友软件官网</a>
		</span>
		<span>
		<a href="http://weibo.com/yongyou">用友集团官方微博</a>
		</span>
		<span>客户热线：010-62432134</span>
		<span style="display: none;" id="returnmobile">
		<a href="http://udn.yyuap.com/forum.php?mobile=2">手机触屏版</a>
		</span>
		</div>
		<div>
		<span>版权所有：用友软件股份有限公司82041</span>
		<span><a target="_blank" href="http://www.beianbeian.com/beianxinxi/7000f338-b528-4ab1-bdf8-45fd65de852f.html">京ICP备05007539号-11<a></span>
		<span>京公网网安备1101080209224</span>
		<span>Powered by Discuz!</span>
		</div>
		</div>
		</div>
		</div>
		</body>
		</html>
		'''

		self.writeFile(htmlStr)

	def writeFile(self,str):
		print "Write String Into File...."
		fp = open(self.filePath,'w')
		fp.write(str)
		fp.close()


def main():
	csp = CreateStaticPage("/root/sourcecode/information_crawler/web","yuqing.html")
	csp.createPage()

if __name__ == '__main__':
	main()
