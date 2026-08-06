# SWAP MEM investigation

## Checks
### Check 1 - Is there "available" RAM
```
free -h
```

### Check 2 - What are the top 10 processes using SWAP [REF](https://www.cyberciti.biz/faq/linux-which-process-is-using-swap/)
```
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | head -10

# Same, but print PID
for file in /proc/*/status; do
  awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file && printf "$(basename $(dirname ${file})) ";
done | sort -k 3 -n -r | head -10
```

### Check 3 - (with process ID) check swap memory usage w/ `VmSwap`
```
grep "VmSwap" /proc/${PID}/status
```

### Check 4 - Further analyze PID in `top`/`htop`
```
top -p ${PID}
```

# Process Profiling

## Query resource usage on process ID
```
htop -p $PID
```

## Grab CPU/MEM usage of all jobs matching a keyword

```
$ KEYWORD="my_command"
$ ps -e -o %cpu,rss,pid,args | awk -v key="${KEYWORD}" '
    BEGIN {
        printf "%-8s %-6s %-10s %s\n", "PID", "%CPU", "MEM(MB)", "COMMAND"
        print "--------------------------------------------------------------------------------"
    }
    $0 ~ key && !/awk/ {
        cpu += $1
        rss_kb += $2
        count++

        mem_mb = $2 / 1024

        cmd = ""
        for (i = 4; i <= NF; i++) cmd = cmd " " $i

        printf "%-8s %-6.1f %-10.1f %s\n", $3, $1, mem_mb, substr(cmd, 2)
    }
    END {
        print "--------------------------------------------------------------------------------"
        printf "Processes tracked: %d\n", count
        printf "Total CPU: %.2f%%\n", cpu
        printf "Total MEM: %.2f MB (%.2f GB)\n", rss_kb / 1024, rss_kb / (1024 * 1024)
    }
'
```

