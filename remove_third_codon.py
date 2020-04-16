#!/usr/bin/env python

import sys


with open(sys.argv[1]) as f:
	lst=[]
	for s in f.readlines():
		if s.startswith(">"):
			lst.append(s)
		else:
			newstring = ''.join("-" if j % 3 == 0 else char for j, char in enumerate(s, 1))
			lst.append(newstring)
	sys.stdout.write("".join(lst))
	
