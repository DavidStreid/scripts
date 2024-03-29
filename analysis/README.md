# Analysis
Helpful tools - I like to make an alias for them like below -
```
$ cat ~/.bash_profile
alias graph_csv='python3 PATH/TO/scripts/analysis/graph_nums.py'
alias classify='python3 PATH/TO/scripts/analysis/test_classifiers.py'

$ graph_csv training.csv			# Graph all features alone
$ classify training.csv test.csv category	# Test KNN, Random-forest, svm, logitstic regression on training
```

## Test classifiers (`test_classifiers.py`)
### Inputs
* `training file`: `*.csv` (required), comma-separated file containing features and label
  > ``` 
  > $ cat training.csv
  > f1,f2,category
  > 0,1,1
  > 1,0,0
  > 0,0,2
  > ...
  > ```
* `test file`: `*.csv` (required) - comma-separated file w/ features 
  > ``` 
  > $ cat test.csv
  > f1,f2
  > 1,1
  > 0,1
  > 0,0
  > ...
  > ```
* `label-column`: string (optional) - exact string of column that is the label
  > Eg: `category`
* `[features]`: list of strings (optional) - list of exact strings of columns that you would like to put into a classifier
  > Eg: `f1 f2`

### Run classifiers
**[1] Show all columns - don't test any classifiers**
```
$ python3 test_classifiers.py \
    -tr ${training_csv} \
    -ts ${test_csv} 
```
**[2] Test classifiers w/ "category" as the label and "f1" & "f2" as the features**
```
$ python3 test_classifiers.py \
    -tr ${training_csv} \
    -ts ${test_csv} \
    -f "f1 f2" \
    -c category
```
**[3] Same as 2, but only print classifiers that label 1 entry as "0", 3 entries as "1", and 5 entries as "2"**
```
$ python3 test_classifiers.py \
    -tr ${training_csv} \
    -ts ${test_csv} \
    -f "f1 f2" \
    -c category \
    -e "0:1,1:3,2:5"
```
**[4] 3 but w/ wiggle - only print classifiers that label 0-2 entries as "0", 2-4 entries as "1", and 4-6 entries as "2"**
```
$ python3 test_classifiers.py \
    -tr ${training_csv} \
    -ts ${test_csv} \
    -f "f1 f2" \
    -c category \
    -e "1:3,2:5" \
    -w 1 \
```
**[5] Test all classifiers on labelling `category` column w/ all possible combinations of features shared between `training_csv` and `test_csv`**
```
$ python3 test_classifiers.py \
    -tr ${training_csv} \
    -ts ${test_csv} \
    -c category
```

## Graph Numbers (`graph_nums.py`)
### Inputs
* `test file`: `*.csv` (required) - comma-separated file w/ features 
  > ``` 
  > $ cat my_file.txt
  > mean,median,std,file
  > 0.4814276023050369,0.4878048780487805,0.1284245675290927,stat_file.txt
  > ...
  > ```

### Run grapher
```
$ python3 graph_alt_allele_summary.py -f my_file.txt
Input=my_file.txt
	Processing...
		Ignoring column: 'file'
	Graphing...
Done.
$ ls -1 *.pdf
mean___hist.pdf
mean___scatter.pdf
mean___scatter_aggregate.pdf
median___hist.pdf
median___scatter.pdf
median___scatter_aggregate.pdf
std___hist.pdf
std___scatter.pdf
std___scatter_aggregate.pd
```
 
