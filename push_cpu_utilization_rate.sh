#!/bin/sh

while true; do
	cur_date=`date "+%Y-%m-%d %H:%M"`
	cur_ts=`date -d "$cur_date" +%s`
	sample_ts=$((cur_ts - 60))
	val=`python ydns_agent.py -s 10.18.0.166 -c stats -o cycle`
	echo $val > save_cpudata.js
	
	str=`python dealwith_cpu.py`
	val=($str)
	num0_work=${val[0]}
	num1_work=${val[1]}
	num0_recv=${val[2]}
	num1_recv=${val[3]}
		
	curl -X POST --connect-timeout 5 --max-time 5 -d '[{"metric": "cpu_num0_work", "endpoint": "lb4test", "timestamp": '$sample_ts', "step": 60,"value": '$num0_work', "counterType": "GAUGE", "tags": "test"}]' http://127.0.0.1:1988/v1/push
	curl -X POST --connect-timeout 5 --max-time 5 -d '[{"metric": "cpu_num1_work", "endpoint": "lb4test", "timestamp": '$sample_ts', "step": 60,"value": '$num1_work', "counterType": "GAUGE", "tags": "test"}]' http://127.0.0.1:1988/v1/push
	curl -X POST --connect-timeout 5 --max-time 5 -d '[{"metric": "cpu_num0_recv", "endpoint": "lb4test", "timestamp": '$sample_ts', "step": 60,"value": '$num0_recv', "counterType": "GAUGE", "tags": "test"}]' http://127.0.0.1:1988/v1/push
	curl -X POST --connect-timeout 5 --max-time 5 -d '[{"metric": "cpu_num1_recv", "endpoint": "lb4test", "timestamp": '$sample_ts', "step": 60,"value": '$num1_recv', "counterType": "GAUGE", "tags": "test"}]' http://127.0.0.1:1988/v1/push
	sleep 60s
done
