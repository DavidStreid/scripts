# Scripts

Helpfu bash scripts

## Compare TSVs

Compares two TSVs that should have the same headers

```
$ ./compare_tsv.sh new.tsv old.tsv
V1=new.tsv
V2=old.tsv
Sorting new.tsv -> new.tsv_v1
Sorting old.tsv -> old.tsv_v2
COMPARING
1	stable_id	stable_id	SAME
2	dynamic_field_1	dynamic_field_1	DIFFERENT
...
```

## Compare Directory files

Useful when trying to find out what the differences between package installations are

```
./compare_directory_py_files.sh ./I1/py_tool/env ./I2/py_tool/env
```
