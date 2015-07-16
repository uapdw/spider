#!/bin/sh

echo "run information_crawler spiders...."
#for i in JDBaseInfo baidubaijia cbinews ccidnet cctime ceocio chinabyte chinacloud chinamobile ciotimes cnddr csdn csdnactivity ctocio ctociocn dataguru dsj eguan gartner gmw huxiu idc ifeng iresearchNews iresearchReport it168 itbear iteye itpub jinghua leiphone newshexun pcpop qudong sciencechina sina tech163 techqq techweb yesky yidonghua ynet yos zdnet zol
for i in baidubaijia cbinews ccidnet cctime ceocio chinabyte chinacloud chinamobile ciotimes cnddr csdn csdnactivity ctocio ctociocn dataguru dsj eguan gartner gmw huxiu idc ifeng iresearchNews iresearchReport it168 itbear iteye itpub jinghua leiphone newshexun pcpop qudong sciencechina sina tech163 techqq techweb yesky yidonghua ynet yos zdnet zol
do
	curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
done
