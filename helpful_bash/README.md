# Helpful Reference

## [rmdir](https://en.wikipedia.org/wiki/Rmdir)
* Remove directories, but only if empty. i.e. avoid `rm -rf`

## find
* Retrieve files written on a specific day - tricky because interval needs to be >=2, i.e. `-mtime +6 -mtime -7` to look for files written one week ago will return nothing, but `-mtime +6 -mtime -8` will work
```
$ find /mnt/storage/ -mindepth 2 -maxdepth 2 -type d -mtime +0 -mtime -2
```

## rsync
```
rsync -avP     # "a" - always use this, "v" - verbose, "P" - include partial if interrupted and report progress
```

**To check state prior to running**

```
rsync -navui   # "n" - dry-run, "u" - update file if older, "i" itemize, 
rsync -avPu    # Everything looks good, run
```

## compare directories
The following will get files missing from DIR1 that are present in DIR2
```
DIR1=...
DIR2=...
comm -23 <(find ${DIR1} -type f -printf "%P\n" | sort) <(find ${DIR2} -type f -printf "%P\n" | sort) > comm_diff.txt
# comm: -2 to ignore files unique to DIR2, -3 to ignore shared files
# -printf "%P\n": get relative paths
```

## paste
Show columns side by side
```
$ paste <(grep -P "chr1\t100" sample.vcf | cut -f9 | sed 's/:/\n/g' | head) <(grep -P "chr1\t100" sample.vcf | cut -f10 | sed 's/:/\n/g' | head)
GT  0/1
GQ  20
```

*From below,*
```
$ grep -P "chr1\t100" sample.vcf | cut -f9 | sed 's/:/\n/g' | head
GT
GQ
$ grep -P "chr1\t100" sample.vcf | cut -f10 | sed 's/:/\n/g' | head
0/1
20
```

## Formatting `ls`
AWK: `awk '{print $6 "_" $7 "_" $8"\t"$5"\t"$9}'`

```
$ ls -lhtr | awk '{print $6 "_" $7 "_" $8"\t"$5"\t"$9}'
Aug_23_10:14	32B	f1.txt
Aug_23_10:14	55B	f2.txt
Aug_23_10:14	2B	f3.txt
Aug_23_10:17	759K	f4.txt
Aug_23_10:17	246K	f5.txt
Aug_23_10:17	199M	f6.txt
Aug_23_10:14	2G	f7.txt
Aug_23_10:17	246K	f8.txt
Aug_23_10:17	186M	f9.txt
Aug_23_10:14	3B	f10.txt
```

## swap
* **GET TOTAL** using [swap](https://www.cyberciti.biz/faq/linux-which-process-is-using-swap/) & [awk](https://stackoverflow.com/a/25245025/3874247)
```
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | cut -d' ' -f2 | grep -E '[0-9]' |  sort -V  | awk '{s+=$1} END {printf "%.0f\n", s}

# TODO - misses many of the processes that don't output a number of kB
```

## Wrap CMD in time & save time-output
`{ time ${CMD}; } 2> log_time.out`

e.g.
```
CMD="/opt/edico/bin/dragen --bcl-conversion-only true"
CMD+=" --sample-sheet ${SS}"
CMD+=" --bcl-input-directory ${INPUT}"
CMD+=" --output-directory ${OUTPUT}"

echo "${CMD}"
echo "LOG=${LOG}"
{ time ${CMD}; } 2> log_time.out > ${LOG}
```


## Wrapper around logging & running command
```
#########################################
# Executes and logs command
# Arguments:
#   INPUT_CMD - string of command to run, e.g. "picard MarkDuplicates ..."
#########################################
run_cmd () {
  INPUT_CMD=$@
  echo ${INPUT_CMD} >> ${CMD_FILE}
  eval ${INPUT_CMD}
  if [[ $? -ne 0 ]]; then
    # Exit script if command fails
    exit 1   
  fi
}
```
