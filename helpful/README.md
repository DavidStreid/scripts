# Helpful Reference

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
