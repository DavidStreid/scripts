# Helpful Reference

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
