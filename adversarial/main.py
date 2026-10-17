# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/15/2026
# project3
# main.py

import sys
from parser import parse

#saves cla 
algorithm = sys.argv[1]
depth = int(sys.argv[2])

#reads one state per line until the file ends
for line in sys.stdin:
    #skips blank lines
    if not line.strip():
        continue
    state = parse(line)