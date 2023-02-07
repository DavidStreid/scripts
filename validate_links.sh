log=link_check.tsv
links=$@

# https://stackoverflow.com/a/29858816/3874247
printf "link\tstatus\n" > ${log}
for link in ${links}; do
  status="FAIL"
  if wget --spider ${link} 2> /dev/null; then
    status="SUCCESS"
  fi
  printf "${link}\t${status}\n" >> ${log}
  sleep 1
done
