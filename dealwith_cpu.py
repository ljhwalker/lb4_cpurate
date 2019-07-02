#!/usr/bin/python

import sys
import json

fw = open("./save_cpudata.js", mode='r')
string = fw.read()
js = json.loads(string)

core = "core-cycles"
num0_worker = "numa0-worker"
num1_worker = "numa1-worker"
num0_recv = "numa0-receiver"
num1_recv = "numa1-receiver"

idle_cycles = "idle_cycles"
work_cycles = "work_cycles"
work_counts = "work_counts"

def get_num():
	global js
	work0 = [0.0,0.0]
	work1 = [0.0,0.0]
	recv0 = [0.0,0.0]
	recv1 = [0.0,0.0]

	keys = js[core].keys()
	for index in range(len(keys)):
		workstr = ""
		if keys[index].find("receiver") != -1:
			workstr = work_counts
		else:
			workstr = work_cycles
	
		idle = float(js[core][keys[index]][idle_cycles])
		work = float(js[core][keys[index]][workstr])
		
		if keys[index].find("numa0-work") != -1:
			work0[0] += idle
			work0[1] += work
		elif keys[index].find("numa1-work") != -1:
			work1[0] += idle
			work1[1] += work
		elif keys[index].find("numa0-receiver") != -1:
			recv0[0] += idle
			recv0[1] += work
		elif keys[index].find("numa1-receiver") != -1:
			recv1[0] += idle
			recv1[1] += work

	print round(work0[1]/(work0[0]+work0[1]),2) \
		,round(work1[1]/(work1[0]+work1[1]), 2) \
		,round(recv0[1]/(recv0[0]+recv0[1]), 2) \
		,round(recv1[1]/(recv1[0]+recv1[1]), 2)

get_num()

