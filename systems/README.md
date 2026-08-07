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

## Profiling spawned processes

Understanding resource usage of processes. Best to use `PGID` vs `PPID` to get the overall resource allocation in case processes spawn other subprocesses

`PPID`, Parent Process ID - ID of the parent process via direct lineage

`PGID`, Process Group ID - ID of the process group leader 

* Helps identify the collection the process belongs to
* children **INHERIT** their parent's `PGID`
* NOTE - for process leader, `PID` == `PGID`

### Process Group ID grouping

```
$ PID="2271455"
$ ps -o pid,pgid,ppid,cmd -p 753582
    PID    PGID    PPID CMD
 753582  753332  753340 python forking.py
$ PGID="753332"
ps -g "${PGID}" -o %cpu,%mem,pgid,pid,args | awk -v gid="${PGID}" '
    $3 == gid {
        cpu += $1
        mem += $2
    }
    END {
        printf "Total CPU: %.2f%%\nTotal MEM: %.2f%%\n", cpu, mem
    }
'
Total CPU: 111.00%
Total MEM: 1.40%
```

### Keyword grouping

Grabs CPU/MEM usage of all jobs matching a keyword, which is useful for processes that are hard to track by groupID, i.e.

* run via containers that are owned by root
* spawned by parallel and Python subprocess that break away from the parent's process group and assign new PGIDs to each spawned worker

NOTES
* `rss` vs `%mem`
  * `rss` (Resident Set Size) - returns actual physical RAM consumed in kilobytes
  * `%mem` -  percentage of total system RAM, which may show as 0.0% if system has lots of RAM

**Example** - grabbing the spawned processes from a `deepvariant` pipeline run in a container via `podman` or `docker`

```
$ KEYWORD="deepvariant"
$ ps -e -o %cpu,rss,pid,args | awk -v key="${KEYWORD}" -v ts="$(date +%s)"  '
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
        printf "RESOURCES\t%s\tProcesses_tracked\t%d\tTotal_CPU\t%.2f\tTotal_MEM\t%.2f MB\t%.2f GB\n", ts, count, cpu, rss_kb / 1024, rss_kb / (1024 * 1024)
    }
'
10001   99.8   718.9      /usr/bin/python3 /tmp/Bazel.runfiles_te6pwa6u/runfiles/com_google_deepvariant/deepvariant/make_examples.py --mode calling --ref...
...
RESOURCES	1786112426	Processes_tracked	52	Total_CPU	1595.60	Total_MEM	12065.73 MB	11.78 GB
```

