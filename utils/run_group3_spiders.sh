#!/bin/sh

echo "run group3 spiders...."
cd /data0/sourcecode/information_crawler/group3
for i in abi baisejiadiantieba bbscheaa cena chmotor ea3w hc360 hea163 jdbbs jdwxinfo newmotor newscheaa smarthomeqianjia zongs_baidu zongs_caam zongs_caijing zongshen_autohome zongshen_bbsmoto8 zongshen_haojue zongshen_lifan zongshen_mallnewmotor zongshen_motorfans zongshen_newmotor zongshen_tieba zongshen_wuyanghonda zongshen_zongshencc zongshen_zongshenmotor zongs_hexun zongs_weixin
do
	#curl http://172.20.8.163:6800/schedule.json -d project=group3 -d spider=${i}
	scrapy crawl $i
done
