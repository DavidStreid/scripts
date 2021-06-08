#!/bin/bash
# Compares the contents of two directories. Returns an error if there are differences and
# shows the differences. Returns a success message if no files are different
# USAGE:  ./compare_dirs.sh ${D1} ${D2}

DIR1=$1
DIR2=$2

if [[ -z ${DIR1} || -z ${DIR2} ]]; then
  echo "Please specify two directories to compare"
  exit 1
fi

if [[ ! -d ${DIR1} ]]; then
  echo "${DIR1} is not a valid directory"
  exit 1
fi

if [[ ! -d ${DIR2} ]]; then
  echo "${DIR2} is not a valid directory"
  exit 1
fi

if [[ ${DIR1} = ${DIR2} ]]; then
  echo "Please provide two different directories"
  exit 1
fi

DIFF_NAME_1=d1.txt
DIFF_NAME_2=d2.txt

DIFF_1=d1md5.txt
DIFF_2=d2md5.txt

find ${DIR1} -type f -exec md5sum {} + | sort -k 2 > ${DIFF_NAME_1}
find ${DIR2} -type f -exec md5sum {} + | sort -k 2 > ${DIFF_NAME_2}

cat ${DIFF_NAME_1} | cut -f1 -d" " > ${DIFF_1}
cat ${DIFF_NAME_2} | cut -f1 -d" " > ${DIFF_2}

if [[ -z $(diff -u ${DIFF_1} ${DIFF_2}) ]]; then
  echo "${DIR1} & ${DIR2} are the same"
else
  echo "ERROR - ${DIR1} & ${DIR2} are different"
  diff -u ${DIFF_NAME_1} ${DIFF_NAME_2}
  ERR=YES
fi

rm ${DIFF_NAME_1}
rm ${DIFF_NAME_2}
rm ${DIFF_1}
rm ${DIFF_2}

if [[ ! -z ${ERR} ]]; then
  exit 1
fi 
