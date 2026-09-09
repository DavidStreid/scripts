#!/bin/bash
# pass the two directories and type of file you are comparing
DIR1=$1
DIR2=$2
SFX=$3

echo "DIR1=${DIR1}"
echo "DIR2=${DIR2}"
echo "SFX=${SFX}"

# 1. Get relative paths from DIR1
files1=$(cd "$DIR1" && find . -type f -name "*.${SFX}")
# 2. Get relative paths from DIR2
files2=$(cd "$DIR2" && find . -type f -name "*.${SFX}")
# 3. Combine and deduplicate into a single list
ALL_FILES=$(printf "%s\n%s\n" "$files1" "$files2" | sort -u)
for file in $ALL_FILES; do
    rel="${file#./}" # remove leading './'
    f1="$DIR1/$rel"
    f2="$DIR2/$rel"
    if [[ ! -f "$f1" ]]; then
        echo "[ADDED]     $rel"
    elif [[ ! -f "$f2" ]]; then
        echo "[MISSING]   $rel"
    elif ! cmp -s "$f1" "$f2"; then
        echo "[DIFFERENT] $rel"
    fi
done
