# SWAP MEM investigation

## Checks
### Check 1 - Is there "available" RAM
```
free -h
```

### Check 2 - What are the top 10 processes using SWAP [REF](https://www.cyberciti.biz/faq/linux-which-process-is-using-swap/)
```
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | head -10
```

### Check 3 - (with process ID) check swap memory usage w/ `VmSwap`
```
grep "VmSwap" /proc/${PID}/status
```

### Check 4 - Further analyze PID in `top`/`htop`
```
top -p ${PID}
```
