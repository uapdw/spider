# -*- coding: utf-8 -*-
import re
import os
import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()
bodyStr = {
	"query":{
		"match":{
			"title":"大数据"
		}
	}
}
res = es.search(index='web-articles',doc_type='article',body=bodyStr,sort="addtime:desc",size=20)

print res
for i in res['hits']['hits']:
	print i["_source"]

print "="*40
print datetime.datetime.now()
print " "
		
fileName = 'yuqing.html'
filePath = os.getcwd() + '/' + fileName
print filePath

htmlStr = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>技术情报 - 用友开发者社区</title>

<meta name="keywords" content="技术情报" />

<meta name="description" content="技术情报" />

<meta name="copyright" content="2001-2013 用友UAP中心" />

<meta name="MSSmartTagsPreventParsing" content="True" />

<meta http-equiv="MSThemeCompatible" content="Yes" />

<base href="http://udn.yyuap.com/" />
<link rel="stylesheet" type="text/css" href="http://udn.yyuap.com/data/cache/style_2_common.css?FPw" />
<link rel="stylesheet" type="text/css" href="http://udn.yyuap.com/data/cache/style_2_portal_list.css?FPw" />
<script type="text/javascript">window.onerror = function() { return true; }; var STYLEID = '2', STATICURL = 'static/', IMGDIR = 'static/image/common', VERHASH = 'FPw', charset = 'utf-8', discuz_uid = '0', cookiepre = '4sun_2132_', cookiedomain = '', cookiepath = '/', showusercard = '1', attackevasive = '0', disallowfloat = 'newthread', creditnotice = '1|专家分|,2|财富值|,3|贡献|,4|饷银|', defaultstyle = '', REPORTURL = 'aHR0cDovL3Vkbi55eXVhcC5jb20vbXpvbmUv', SITEURL = 'http://udn.yyuap.com/', JSPATH = 'data/cache/', DYNAMICURL = '';</script>

<script src="http://udn.yyuap.com/static/js/mobile/jquery-1.8.3.min.js?FPw" type="text/javascript"></script>

<meta name="application-name" content="用友开发者社区" />
<meta name="msapplication-tooltip" content="用友开发者社区" />
<!--网站的图标 -->
<link rel="shortcut icon" href="http://udn.yyuap.com/static/image/common/favicon.ico" type="images/x-icon" />
<link rel="Bookmark" href="http://udn.yyuap.com/static/image/common/favicon.ico">
<link rel="icon" href="http://udn.yyuap.com/static/image/common/favicon.png" type="images/png" />

<meta name="msapplication-task"
content="name=首页;action-uri=http://udn.yyuap.com/portal.php;icon-uri=http://udn.yyuap.com/static/image/common/portal.ico" />
<meta name="msapplication-task"
content="name=论坛;action-uri=http://udn.yyuap.com/forum.php;icon-uri=http://udn.yyuap.com/static/image/common/bbs.ico" />
<link rel="stylesheet" href="http://udn.yyuap.com/template/yongyou/style/css.css" type="text/css" media="screen" charset="utf-8">

<!--UAP63体验CSS  -->
<link rel="stylesheet" type="text/css" href="http://udn.yyuap.com/template/yongyou/style/experience/css/experience.css">

</head>

<body id="nv_portal"
class="pg_list pg_list_2">

<div id="append_parent"></div>
<div id="ajaxwaitid"></div>

<style>
.top_bg_on div{
border-radius:0px;
}
body #box.top_bg_on{
background-color: #fff;
}

#top.top_bg_on, #box.top_bg_on{
margin-left:auto;
margin-right:auto;
width:960px;
padding:10px;
}

#top.top_bg_on{
margin-top:200px; 
background-color:#fff;
border-bottom-left-radius:0px;
border-bottom-right-radius:0px;
}
#box.top_bg_on{
border-top-left-radius:0px;
border-top-right-radius:0px;
}
#toptb{
border-bottom: 0px;
}

.cate_name{
font-size: 21px;
font-family: 'Microsoft YaHei', 微软雅黑, 宋体, Tahoma, Helvetica, 'SimSun',sans-serif;
color: #333333;
}
.sub_cate_name{
font-size: 18px;
font-family: 'Microsoft YaHei', 微软雅黑, 宋体, Tahoma, Helvetica, 'SimSun',sans-serif;
color: #585858;
margin-bottom: 20px;
}

.border-bottom-line{
border-bottom: 1px solid #bbbbbb;
margin-top: 10px;
margin-bottom: 20px;
}

ul.news_list{

}
li.news_item{ 
  list-style: disc inside url('http://information.k.cn:8080/images/dot_03.jpg');
  font-size: 12px;
  font-family: 宋体, Tahoma, Helvetica, 'SimSun',sans-serif;
  color: #585858;
  line-height: 22px;
}
li.news_item_num{
  list-style: none;
  font-size: 12px;
  font-family: 宋体, Tahoma, Helvetica, 'SimSun',sans-serif;
  color: #585858;
  line-height: 22px;
}

.news_area{
  margin-bottom: 30px;
}
.list_block_l{
  width: 350px;
}
.list_block_r{
  width: 290px;
}
</style>

<div id="box" class="wp">
<style id="diy_style" type="text/css"></style>
<!-- CSS -->
<link href="http://udn.yyuap.com/template/yongyou/style/mobile_develop.css" rel="stylesheet" type="text/css" />
<div class="mobile" id="mobile">

   <!-- 轮播图片和热帖排行 -->
   <div class="clearfix top">
        
        <div class="turn l">
         <div class="cate_name">技术动态</div>
         <div class="border-bottom-line"></div>
         <div class="news_area clearfix">
          <div class="l list_block_l">
            <div class="sub_cate_name">大数据</div>
            <div class="">
              <ul class="">
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
              </ul>
            </div>
          </div>
          <div class="r list_block_r">
            <div class="sub_cate_name">大数据</div>
            <div>
              <ul class="">
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
              </ul>
            </div>
          </div>
         </div> 
         <div class="news_area clearfix">
         	<div class="l list_block_l">
         		<div class="sub_cate_name">大数据</div>
         		<div>
         			<ul class="">
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
	         			<li class="news_item">大数据大数据大数据</li>
	         		</ul>
         		</div>
         	</div>
         	<div class="r list_block_r">
            <div class="sub_cate_name">大数据</div>
            <div>
              <ul class="">
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
                <li class="news_item">大数据大数据大数据</li>
              </ul>
            </div>
          </div>
         </div>
        </div>
        
        <div class="sort r">
           <div class="cate_name">用友动态</div>
           <div class="border-bottom-line"></div>
           <div>
              <ul class="">
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
                <li class="news_item_num">大数据大数据大数据</li>
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

fp = open(filePath,'w')
fp.write(htmlStr)
fp.close()




