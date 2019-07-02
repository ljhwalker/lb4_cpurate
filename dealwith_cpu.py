#!/usr/bin/python

import sys
import json

def get_num(Js):
	work0 = [0.0,0.0]
	work1 = [0.0,0.0]
	recv0 = [0.0,0.0]
	recv1 = [0.0,0.0]
	
	Core = "core-cycles"
	Idle_Cycles = "idle_cycles"
	Work_Cycles = "work_cycles"
	Work_Counts = "work_counts"

	keys = Js[Core].keys()
	for index in range(len(keys)):
		workstr = ""
		if keys[index].find("receiver") != -1:
			workstr = Work_Counts
		else:
			workstr = Work_Cycles
	
		idle = float(Js[Core][keys[index]][Idle_Cycles])
		work = float(Js[Core][keys[index]][workstr])
		
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

def main():
	Fw = open("./save_cpudata.js", mode='r')
	String = Fw.read()
	Js = json.loads(String)
	get_num(Js)

if __name__ == "__main__":
	sys.exit(main())
