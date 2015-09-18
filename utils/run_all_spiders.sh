#!/bin/sh


echo "run information_crawler spiders...."
cd /data0/sourcecode/information_crawler/infomation_crawler
for i in  baidubaijia cbinews ccidnet cctime ceocio chinabyte chinacloud chinamobile ciotimes cnddr csdn csdnactivity ctocio ctociocn dataguru dsj eguan gartner gmw huxiu idc ifeng iresearchNews iresearchReport it168 itbear iteye itpub jinghua leiphone newshexun pcpop qudong sciencechina sina tech163 techqq techweb yesky yidonghua ynet yos zdnet zol article_100ec article_kn58 article_myzaker article_s3d4 article_tsci article_toutiao article_cbismb article_doit article_ceweekly article_huanqiu article_xinmin article_gmw article_chinacaixin blog_sina weibo_sina article_sohu_it article_qq_finance article_spn_news
do
	#curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
	scrapy crawl $i
done

echo "run create_indexs_bulk_from_hbase.py ...."
/root/.virtualenvs/scrapy0.24.5/bin/python /data0/sourcecode/information_crawler/utils/create_indexs_bulk_from_hbase.py

echo "run group3 spiders...."
cd /data0/sourcecode/information_crawler/group3
for i in zongshen_mallnewmotor hc360 abi baisejiadiantieba bbscheaa cena chmotor ea3w hea163 jdbbs jdwxinfo newmotor newscheaa smarthomeqianjia zongs_baidu zongs_caam zongs_caijing zongshen_autohome zongshen_bbsmoto8 zongshen_haojue zongshen_lifan zongshen_motorfans zongshen_newmotor zongshen_tieba zongshen_wuyanghonda zongshen_zongshencc zongshen_zongshenmotor zongs_hexun zongs_weixin
do
	#curl http://172.20.8.163:6800/schedule.json -d project=group3 -d spider=${i}
	scrapy crawl $i
done

echo "run JD spiders...."
cd /data0/sourcecode/information_crawler/infomation_crawler
for i in JDBaseInfo JDCommDetail JDDpInfoTest JDSummaryComm JDWaresInfoTest
do
	#curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
	scrapy crawl $i
done
