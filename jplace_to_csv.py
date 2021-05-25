#! /usr/bin/env python
import json,sys
j=json.load(sys.stdin); 
for pl in j['placements']:
	sys.stdout.write(pl["n"][0] + "\t") 
	sys.stdout.write(str(pl["p"][0][0]) + "\t") 
	sys.stdout.write(str(pl["p"][0][1]) + "\t") 
	sys.stdout.write(str(pl["p"][0][3]) + "\t") 
	sys.stdout.write(str(pl["p"][0][4]) + "\n") 



