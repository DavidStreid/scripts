#!/usr/bin/env bash

V1=$1
V2=$2

echo "V1=${V1}"
echo "V2=${V2}"
if [[ ! -f ${V1} || ! -f ${V2} ]]; then
  echo "Invalid files"
  exit 1
fi

base_v1=$(basename ${V1})
V1_SORTED="${base_v1}_v1"
echo "Sorting ${base_v1} -> ${V1_SORTED}"
head -1 ${V1} > ${V1_SORTED}
tail -n+2 ${V1} | sort >> ${V1_SORTED}

base_v2=$(basename ${V2})
V2_SORTED="${base_v2}_v2"
echo "Sorting ${base_v2} -> ${V2_SORTED}"
head -1 ${V2} > ${V2_SORTED}
tail -n+2 ${V2} | sort >> ${V2_SORTED}

# Grab the minimum column count to compare between the two files
num_cols1=$(awk -F'\t' 'NR==1{print NF}' "${V1}")
num_cols2=$(awk -F'\t' 'NR==1{print NF}' "${V2}")
(( min_cols = num_cols1 < num_cols2 ? num_cols1 : num_cols2 )) 

echo "Comparing up to column ${min_cols} (new: ${num_cols1}, old: ${num_cols2})"

for ((i=1; i<=min_cols; i++)); do
  c_col=$(head -1 ${V2_SORTED} | cut -f${i})
  o_col=$(head -1 ${V1_SORTED} | cut -f${i})
  out=col${i}.txt
  diff <(cut -f${i} ${V1_SORTED}) <(cut -f${i} ${V2_SORTED}) > ${out}
  d=$(wc -l ${out} | sed 's/^  *//g' | sed 's/  */\t/g' | cut -f1)
  if [[ ${d} -gt 0 ]]; then
    printf "${i}\t${c_col}\t${o_col}\tDIFF\n"
  else
    printf "${i}\t${c_col}\t${o_col}\tSAME\n"
    rm ${out}
  fi
done 2>&1 | tee comparison.tsv
