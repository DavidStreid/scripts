
# RUN
```
$ cat my_file.txt
mean,median,std
0.4814276023050369,0.4878048780487805,0.1284245675290927
...
$ python3 graph_alt_allele_summary.py my_file.txt
Input=my_file.txt
	Processing...
	Graphing...
Done.
$ ls -1 *.pdf
mean___hist.pdf
mean___scatter.pdf
mean___scatter_aggregate.pdf
median___hist.pdf
median___scatter.pdf
median___scatter_aggregate.pdf
std___hist.pdf
std___scatter.pdf
std___scatter_aggregate.pd
```
