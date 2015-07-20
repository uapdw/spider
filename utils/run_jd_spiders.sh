echo "run JD spiders...."
cd /data0/sourcecode/information_crawler/infomation_crawler
for i in JDBaseInfo JDCommDetail JDDpInfoTest JDSummaryComm JDWaresInfoTest
do
	#curl http://172.20.8.162:6800/schedule.json -d project=infomation_crawler -d spider=${i}
	scrapy crawl $i
done
