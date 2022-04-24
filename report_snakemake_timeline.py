#! /usr/bin/env python

import sys
import re
import time 
event = []
active_jobs={}

tzero=0
cpucounter=0
for line in sys.stdin.readlines():
    if line.startswith("[") or "Complete log" in line:
        # start a new event
        if not event:
            event = [line]
            asctime = time.strptime(event[0].strip().replace("[","").replace("]",""))
            epoch = time.mktime(asctime)
            tzero=epoch
            continue
        # process previous event
        else:
            event_text = '\n'.join(event)
            asctime = time.strptime(event[0].strip().replace("[","").replace("]",""))
            epoch = time.mktime(asctime)
            event_time=epoch-tzero
            if "done" in event_text and "cpus" not in event_text:
                jobid = re.search("Finished job ([0-9]+).", event_text).groups()[0]    
                cpucounter -= active_jobs[jobid]
                print("finish\t%s\t%d\t%s\t%d\t%d" % ("rule", int(event_time),jobid, -active_jobs[jobid], cpucounter))
            elif "cpus" in event_text:
                jobid = re.search("jobid: ([0-9]+)", event_text).groups()[0]
                cpus = re.search("cpus=([0-9]+)", event_text).groups()[0]
                rulename = event[1].split(" ")[1][:-2]
                active_jobs[jobid] = int(cpus)
                cpucounter += active_jobs[jobid]
                print("start\t%s\t%d\t%s\t%d\t%d" % (rulename, event_time, jobid, int(cpus), cpucounter))
            event = [line]
    else:
        if event:
            event += [line]

