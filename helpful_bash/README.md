# Helpful Reference

## Options

***Strict mode***
```
set -euo pipefail     # -e:          Exit script if command fails  
                      # -u:          Unset variables cause error
                      # -o pipefail: failures within pipe cause error
 ```

***Log Commands***
```
set -x    # log commands
set +x    # end logging
```

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

## `comm`
Given two sorted files, return entries unique (`-23` or `-13`) to each and shared in both (`-12`)

```
comm -23 f1.txt f2.txt # Only in File 1
comm -13 f1.txt f2.txt # Only in File 2
comm -12 f1.txt f2.txt # In Both
```

### compare directories
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

helpful function - pivot a TSV into a vertical key-value list
```
peek() {
  paste <(head -n 1 "$1" | tr '\t' '\n') <(tail -n 1 "$1" | tr '\t' '\n')
}
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

## `jq` - json grep
**Download**
```
wget https://github.com/Illumina/ExpansionHunter/blob/master/variant_catalog/hg38/variant_catalog.json
```

**Parsing fields**
```
$ jq -r '.[] | {LocusId, ReferenceRegion}' regions.json | head
{
  "LocusId": "AFF2",
  "ReferenceRegion": "chrX:148500631-148500691"
}
...
```

**Formatting**
```
$ jq -r '.[] | "\(.LocusId)\t\(.ReferenceRegion)"'  variant_catalog.json
AFF2	chrX:148500631-148500691
...
```

**Filtering**
```
$ jq -r '.[] | select(.LocusId == "FMR1") | "\(.LocusId)\t\(.ReferenceRegion)"'    regions.json
FMR1	chrX:147912050-147912110
```

## `xargs`

No args - `... | xargs <CMD> ...`, potentially not safe and batches all args to run `CMD` once

### `... | xargs -I {} <CMD> {} ...` - run piped command on each delimited output

* NOTE - `{}` is just a placeholder, can be any set of characters

```
find ... | xargs -I {} mv {} /backup/
```

Or, in batches (sort every set of 5 files)
```
find . -type f | xargs -n 5 echo | sort
```

### `find ... print0 | xargs -0 ...` - safely piping from `find`

* end every file w/ a null character
* expect null character delimiter

```
find . -type f print0 | xargs -0 ls
```

## `awk`
### Sum list of numbers

Pipe to `... | awk '{sum += $1} END {print sum}'`

```
$ for i in {1..10}; do echo ${i}; done | awk '{sum += $1} END {print sum}'
55
```

### Formatting `ls`
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

### swap
* **GET TOTAL** using [swap](https://www.cyberciti.biz/faq/linux-which-process-is-using-swap/) & [awk](https://stackoverflow.com/a/25245025/3874247)
```
for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | cut -d' ' -f2 | grep -E '[0-9]' |  sort -V  | awk '{s+=$1} END {printf "%.0f\n", s}

# TODO - misses many of the processes that don't output a number of kB
```

## `while`

**Best Practices**
- specify delimiter, i.e. Internal Field Separator, or `IFS`
- redirection - efficient and allows for custom file descriptors, e.g. `read line <&3` & `3< file.txt`

e.g. reading a TSV
```
cat data.tsv
# 4	5
while IFS=$'\t' read c1 c2 <&3; do
  echo "$c1 + $c2 = $((c1 + c2))"
done 3< data.tsv
# 4 + 5 = 9
```

## [`parallel`](https://www.gnu.org/software/parallel/parallel_examples.html)

```
OUT="./ws"             # this will log workspace
LOG="cmd_status.tsv"    
parallel --results "$OUT" \
         --joblog "$LOG" \
         --jobs 15 \
         "echo 'Processing number: {}'" ::: {1..100} # :::: nums.txt # <- (for file input)
```

***outputs***

```
$ head cmd_status.tsv
Seq	Host	Starttime	JobRuntime	Send	Receive	Exitval	Signal	Command
1	:	1776871386.217	     0.022	0	21	0	0	echo 'Processing number: 1'
2	:	1776871386.221	     0.023	0	21	0	0	echo 'Processing number: 2'
...
$ tree ws/ | head
ws/
└── 1
    ├── 1
    │   ├── seq
    │   ├── stderr
    │   └── stdout
    ├── 10
    ...
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

simple way - `set -x` (start logging) & `set +x` (stop logging)
```
$ echo "hello world"
+ echo 'hello world'
hello world
$ set +x
+ set +x
$ echo "done."
done.
```

Custom formatting - use a function
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
