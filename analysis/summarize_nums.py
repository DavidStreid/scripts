import pandas as pd
import sys

f = sys.argv[1] # e.g. 'for i in {1..10}; do echo ${i}; done > f.txt'

counts = []
with open(f, 'r') as in_f:
  for line in in_f:
    num = int(line.strip())
    counts.append(num)

s = pd.Series(counts)
print(s.describe())

