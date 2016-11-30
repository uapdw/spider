#!/bin/bash

for n in "cninfo_com_cn_listed_corp_info" "cninfo_com_cn_balance" "cninfo_com_cn_profit" "cninfo_com_cn_cashflow"
do
    nohup /root/.virtualenvs/spider/bin/scrapy crawl $n > /data0/log/$n.log 2>&1 &
done
