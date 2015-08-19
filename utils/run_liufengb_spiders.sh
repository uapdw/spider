#!/bin/sh


echo "run information_crawler spiders...."
cd /data0/sourcecode/information_crawler/group3
#for i in zongshen_autohome zongshen_bbsmoto8 zongshen_motorfans zongshen_newmotor zongshen_tieba zongshen_zongshenmotor zongshen_haojue zongshen_lifan zongshen_wuyanghonda zongshen_zongshencc 
for i in zongshen_mallnewmotor
do
        #curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
        scrapy crawl $i
done
