#!/bin/sh


echo "run information_crawler spiders...."
cd /data0/sourcecode/information_crawler/infomation_crawler
for i in  baidubaijia cbinews ccidnet cctime ceocio chinabyte chinacloud chinamobile ciotimes cnddr csdn csdnactivity ctocio ctociocn dataguru dsj eguan gartner gmw huxiu idc ifeng iresearchNews iresearchReport it168 itbear iteye itpub jinghua leiphone newshexun pcpop qudong sciencechina sina tech163 techqq techweb yesky yidonghua ynet yos zdnet zol
do
	#curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
	scrapy crawl $i
done

echo "run create_indexs_bulk_from_hbase.py ...."
/root/.virtualenvs/scrapy0.24.5/bin/python /data0/sourcecode/information_crawler/utils/create_indexs_bulk_from_hbase.py

echo "run group3 spiders...."
cd /data0/sourcecode/information_crawler/group3
for i in abi baisejiadiantieba bbscheaa cena ea3w hc360 hea163 jdbbs jdwxinfo newscheaa smarthomeqianjia
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
