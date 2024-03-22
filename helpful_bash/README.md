# Helpful Reference

## [rmdir](https://en.wikipedia.org/wiki/Rmdir)
* Remove directories, but only if empty. i.e. avoid `rm -rf`

## find
* Retrieve files written on a specific day - tricky because interval needs to be >=2, i.e. `-mtime +6 -mtime -7` to look for files written one week ago will return nothing, but `-mtime +6 -mtime -8` will work
```
$ find /mnt/storage/ -mindepth 2 -maxdepth 2 -type d -mtime +0 -mtime -2
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
