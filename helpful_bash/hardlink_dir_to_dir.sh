#!/bin/bash

SRC=$1
TGT=$2

echo "SRC=${SRC}"
echo "TGT=${TGT}"
if [[ ! -d ${SRC} || ! -d ${TGT} ]]; then
  echo "INVALID"
  exit 1
fi
if [[ ! -z "$(ls -A "$TGT")" ]]; then
  echo "${TGT} is not empty"
fi

for f in $(find ${SRC} -mindepth 1 -maxdepth 1 -type f); do
  tgt="${TGT}/$(basename ${f})"
  echo "ln ${f} ${tgt}"
done
