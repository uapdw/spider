#!/bin/bash

cd /data0/sourcecode/spider/current/;
source ~/.bash_profile;
workon spider;
for n in "szse_cn_curr_listed_corp" "sse_com_cn_sh_listed_corp_info" "cninfo_com_cn_curr_listed_corp"
do
    scrapy crawl $n > /data0/log/$n.log 2>&1
done
