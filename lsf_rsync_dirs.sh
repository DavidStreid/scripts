#!/bin/bash
# Copies all directories (one level deep) in a source directory to their target direcotry in parallel

SCRIPT=$0
LOCATION=$(dirname ${SCRIPT})
SOURCE=$1
TARGET=$2

LOG="${LOCATION}/rsync_log.out"

echo "Moving directories in ${SOURCE} to ${TARGET}. Logging to ${LOG}"

DIRS=$(find ${SOURCE} -mindepth 1 -maxdepth 1 -type d)
NUM_DIRS=$(echo ${DIRS} | tr ' ' '\n' | wc -l)

echo "Found ${NUM_DIRS} directories"

for dir in ${DIRS}; do
  dName=$(basename ${dir})
  job_name="RSYNC___${dName}"
  echo "Running ${job_name} - Moving ${dir}"

  CMD="rsync -a ${dir} ${TARGET}"
  BSUB="bsub -J ${job_name} -o ${job_name}.out -n 20 -M 4 ${CMD}"

  echo ${BSUB} >> ${LOG}
  eval ${BSUB} >> ${LOG}
  
  exit 0
done
