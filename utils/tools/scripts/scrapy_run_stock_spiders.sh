#!/bin/bash

cd /data0/sourcecode/spider/current/;
source ~/.bash_profile;
workon spider;
for n in "cninfo_com_cn_listed_corp_info" "cninfo_com_cn_balance" "cninfo_com_cn_profit" "cninfo_com_cn_cashflow"
do
    nohup scrapy crawl $n > /data0/log/$n.log 2>&1 &
done
