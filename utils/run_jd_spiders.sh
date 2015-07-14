#!/bin/sh

echo "run JD spiders...."
for i in JDCommDetail JDDpInfoTest JDSummaryComm JDWaresInfo JDWaresInfoTest
do
	curl http://172.20.8.162:6800/schedule.json -d project=group3 -d spider=${i}
done
