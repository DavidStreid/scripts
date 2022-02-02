import argparse
from os.path import exists
import sys
# knn
from sklearn.neighbors import KNeighborsClassifier
# random forst
from sklearn.ensemble import RandomForestClassifier
# SVM
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
# Logistic Regression
from sklearn.linear_model import LogisticRegression
# For testing all possible feature combinations
import itertools

DELIMITER = ','


def train_logistic_regression(x, y):
  clf = LogisticRegression(random_state=0).fit(x, y)
  
  return clf

def train_knn(x, y, n_neighbors):
  neigh = KNeighborsClassifier(n_neighbors=n_neighbors)
  neigh.fit(x, y)

  return neigh

def tran_random_forest(x, y, max_depth):
  clf = RandomForestClassifier(max_depth=max_depth, random_state=0)
  clf.fit(x, y)

  return clf

def train_svm(x, y):
  clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
  clf.fit(x,y)

  return clf

def get_all_feature_combinations(feature_list):
  combinations = []
  for i in range(1,len(feature_list)+1):
    combinations.extend(list(itertools.combinations(feature_list,i)))
  return combinations

def get_columns(f_name):
  cols = []
  with open(f_name, 'r') as summary_in:
    for line in summary_in:
      cleaned = line.strip()
      vals = cleaned.split(DELIMITER)
      cols.append(vals)

  if len(cols) == 0:
    print("ERROR - empty file")
    sys.exit(1)

  num_cols_list = list(set([ len(vals) for vals in cols ]))
  if len(num_cols_list) > 1:
    print("WARNING - some lines have unexpected values")
  num_cols = sorted(num_cols_list)[0]

  list_of_col_values = []
  for col in range(num_cols):
    l = [ line[col] for line in cols ]
    list_of_col_values.append(l)

  categorical_columns = []

  numerical_columns = []
  for col_vals in list_of_col_values:
    headers = [ val for val in col_vals if not is_float(val) ]
    if len(headers) == 1:
      header = headers[0]
    else:
      header = None
    if len(headers) == len(col_vals):
      # Track columns w/ just words - won't be used for classification
      categorical_columns.append([ col_vals[0], col_vals[1:] ])
    else:
      vals = [ float(val) for val in col_vals if is_float(val) ]
      numerical_columns.append( [ header, vals ] ) 

  val_len = set([ len(line[1]) for line in numerical_columns ])
  if len(val_len) != 1:
    print("\t[ERROR] - Invalid value columns")
    sys.exit(1)

  return numerical_columns, categorical_columns, list(val_len)[0]

def is_float(element: any) -> bool:
    # https://stackoverflow.com/a/20929881/3874247
    try:
        float(element)
        return True
    except ValueError:
        return False


def get_feature_indices(header_vals_list, features):
  all_headers = [ val[0] for val in header_vals_list ]
  all_headers_set = set(all_headers)

  valid_featuers = True
  features_idx = []
  for feature in features:
    if feature not in all_headers_set:
      print("\t[ERROR] Invalid feature column: %s" % feature)
      valid_featuers = False
    else:
      features_idx.append(all_headers.index(feature))
  if not valid_featuers:
    sys.exit(1)

  return features_idx


def get_feature_and_category_indices(header_vals_list, category, features):
  all_headers = [ val[0] for val in header_vals_list ]
  all_headers_set = set(all_headers)
  if category not in all_headers_set:
    print("\t[ERROR] Invalid category column: %s" % category)
    sys.exit(1)

  valid_featuers = True
  features_idx = []
  for feature in features:
    if feature not in all_headers_set:
      print("\t[ERROR] Invalid feature column: %s" % feature)
      valid_featuers = False
    else:
      features_idx.append(all_headers.index(feature))

  if not valid_featuers:
    sys.exit(1)

  category_idx = all_headers.index(category)

  return category_idx, features_idx

def get_x(header_vals_list, num_vals, features_idx):
  x = []
  for i in range(num_vals):
    x_entry = [ header_vals_list[idx][1][i] for idx in features_idx ]
    x.append(x_entry)
  return x

def get_x_and_y(header_vals_list, num_vals, features_idx, category_idx):
  x = []
  for i in range(num_vals):
    x_entry = [ header_vals_list[idx][1][i] for idx in features_idx ]
    x.append(x_entry)
  y = header_vals_list[category_idx][1]
  return x, y

def write_cols_to_file(categorical_columns, numerical_columns, prediction_columns, out_file):
  header_vals_list = []
  header_vals_list.extend(categorical_columns)
  header_vals_list.extend(numerical_columns)
  header_vals_list.extend(prediction_columns)
  with open(out_file, 'w') as out:
    header = [ col[0] for col in header_vals_list ]
    values = [ col[1] for col in header_vals_list ]

    all_col_lengths = list(set([len(col_vals) for col_vals in values]))
    if len(all_col_lengths) != 1:
      print("[WARNING] Invalid number of input values - [ %s ]" % ', '.join([str(val) for val in all_col_lengths]))

    out.write(f"{','.join(header)}\n")
    for i in range(all_col_lengths[0]):
      line = f"{','.join([ str(value[i]) for value in values ])}\n"
      out.write(line)

def run_predictions(x, y, x_test, expected_dic, wiggle):
  prediction_list = []

  models = [
    [ 'knn_5', train_knn(x, y, 5) ],
    [ 'knn_4', train_knn(x, y, 4) ],
    [ 'knn_3', train_knn(x, y, 3) ],
    [ 'knn_2', train_knn(x, y, 2) ],
    [ 'knn_1', train_knn(x, y, 1) ],
    [ 'rf_1', tran_random_forest(x, y, 5) ],
    [ 'rf_1', tran_random_forest(x, y, 4) ],
    [ 'rf_1', tran_random_forest(x, y, 3) ],
    [ 'rf_1', tran_random_forest(x, y, 2) ],
    [ 'rf_1', tran_random_forest(x, y, 1) ],
    [ 'svm', train_svm(x, y) ],
    [ 'log_reg', train_logistic_regression(x, y) ]
  ]
  
  if expected_dic:
    print(f"\tOnly printing classifiers that have the following counts (+/- {wiggle}) - {expected_dic}")

  for model_pair in models:
    model_label = model_pair[0]
    model = model_pair[1]
    predictions = []
    prediction_report = {}
    for x_t in x_test:
      prediction = model.predict([x_t])
      prediction_label = prediction[0]
      predictions.append(prediction_label)

      if prediction_label in prediction_report:
        prediction_report[prediction_label] += 1
      else:
        prediction_report[prediction_label] = 1

    if expected_dic:
      if is_expected(expected_dic, prediction_report, wiggle):
        print(f"\t\tSUCCESS - [{model_label}] Classifications (n={len(x_test)})")
      else:
        continue
    else:
      print(f"\t[{model_label}] Classifications (n={len(x_test)})")
      for k,v in prediction_report.items():
        print(f'\t\t{k}: {v}')

    prediction_col = [model_label, predictions]
    prediction_list.append(prediction_col)

  return prediction_list


def is_expected(expected_dic, prediction_report, wiggle):
  prediction_report_keys = set([ str(key) for key in list(prediction_report.keys()) ])

  # Check that everything in the expected dic will be checked by iterating over the shared keys
  for expected_category, expected_count in expected_dic.items():
    if expected_category not in prediction_report_keys and expected_count != 0:
      # labels that aren't assigned won't be present in the prediction report - if 0 is expected, then it not being present is ok
      return False
  for category, count in prediction_report.items():
    key = str(category)
    if key in expected_dic:
      # It's ok for the expected dic to not have a key - the dic can mention as many or a few keys as desired
      min = count - wiggle
      max = count + wiggle
      if expected_dic[key] < min or expected_dic[key] > max:
        # Get range around which the actual value is allowed
        return False

  return True

def run_predictions_on_category_and_features(category, features, numerical_column_list, num_vals, test_numerical_column_list, test_num_vals, test_categorical_column_list, expected_dic, wiggle):
  out_file = f"{category}_predictions___{'_'.join(features)}.csv"
  # print("Training...")
  category_idx, features_idx = get_feature_and_category_indices(numerical_column_list, category, features)
  x, y = get_x_and_y(numerical_column_list, num_vals, features_idx, category_idx)

  # print("Extracting test set...")
  features_idx = get_feature_indices(test_numerical_column_list, features)
  x_test = get_x(test_numerical_column_list, test_num_vals, features_idx)

  # print("Running classifiers...")
  prediction_list = run_predictions(x, y, x_test, expected_dic, wiggle)

  if len(prediction_list) > 0:
    write_cols_to_file(test_categorical_column_list, test_numerical_column_list, prediction_list, out_file)

def validate_inputs(training_file, test_file, category, features, expected_counts, wiggle):
  errors = []
  if not exists(training_file):
    errors.append(f'Invalid training file: {training_file}')
  if not exists(test_file):
    errors.append(f'Invalid test file: {training_file}')
  if features is not None and category is None:
    errors.append('Define category column for features')
  if expected_counts is not None:
    if features is None or category is None:
      errors.append('Define category/feature column(s)')
    dic = get_expected_dictionary(expected_counts)
    if len(dic) == 0:
      errors.append(f"Invalid format for expected_counts, e.g. 'k1:v1,k2:v2' where all v* are ints: {expected_counts}")
  if wiggle is not None:
    if not wiggle.isnumeric():
      errors.append(f"Wiggle parameter should be an integer. Got {wiggle}")
  if len(errors) > 0:
    print("ERRORS")
    for err in errors:
      print(f'\t{err}')
    sys.exit(1)




def get_expected_dictionary(expected_counts):
  dic = {}
  category_count_list = expected_counts.split(',')
  for cat_ct in category_count_list:
    cat_ct_pair = cat_ct.split(':')
    if len(cat_ct_pair) != 2:
      return {}
    [category, count] = cat_ct_pair
    if not count.isnumeric():
      return {}
    dic[category] = int(count)
  return dic

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Teset classifiers')
  parser.add_argument('-tr', dest='training_file', help='training file - features & categories (.csv)', required=True)
  parser.add_argument('-ts', dest='test_file', help='test file - features (.csv)', required=True)
  parser.add_argument('-c', dest='category', help='exact text of category column in training & test file', default=None)
  parser.add_argument('-f', dest='features', help='exact text of category column in training & test file', default=None)
  parser.add_argument('-e', dest='expected_counts', help='comma-separated key:value pairs of expected number of categorized entries, e.g. "label1:count,label2:count"', default=None)
  parser.add_argument('-w', dest='wiggle', help='range around each expected count allowed', default='0')

  args = parser.parse_args()
  training_file = args.training_file
  test_file = args.test_file
  category = args.category
  features = args.features
  expected_counts = args.expected_counts
  wiggle = args.wiggle

  validate_inputs(training_file, test_file, category, features, expected_counts, wiggle)

  print("Inputs")
  print("\ttrain: %s" % training_file)
  print("\ttest: %s" % test_file)
  if category is not None:
    print("\tcategory: %s" % category)
  feature_list = None
  if features is not None:
    feature_list = sorted(features.split(" "))
    print("\tfeatures (num=%s): [ %s ]" % (len(feature_list), ', '.join(feature_list)))
  expected_dic = None
  if expected_counts is not None:
    expected_dic = get_expected_dictionary(expected_counts)
    print(f"\texpected: {expected_dic}")
  if wiggle is not None:
    wiggle = int(wiggle)
    print(f"\twiggle: +/-{wiggle}")
    
  numerical_column_list, categorical_column_list, num_vals = get_columns(training_file)
  test_numerical_column_list, test_categorical_column_list, test_num_vals = get_columns(test_file)

  if category and feature_list:
    run_predictions_on_category_and_features(category, feature_list, numerical_column_list, num_vals, test_numerical_column_list, test_num_vals, test_categorical_column_list, expected_dic, wiggle)
  elif category and not feature_list:
    numerical_column_headers = set([ col[0] for col in numerical_column_list ])
    test_numerical_column_headers = set([ col[0] for col in test_numerical_column_list ])
    shared_headers = list(numerical_column_headers.intersection(test_numerical_column_headers))
    feature_combinations = get_all_feature_combinations(shared_headers)
    print(f"{len(shared_headers)} shared features. Testing {len(feature_combinations)} feature combinations...")
    for feature_combo in feature_combinations:
      run_predictions_on_category_and_features(category, feature_combo, numerical_column_list, num_vals, test_numerical_column_list, test_num_vals, test_categorical_column_list, expected_dic, wiggle)
  else:
    # If only two files are passed - just get the columns that could be features/categories
    all_train_headers = set([ val[0] for val in numerical_column_list ])
    all_test_headers = set([ val[0] for val in test_numerical_column_list ])

    shared_headers = list(all_train_headers.intersection(all_test_headers))
    print("Possible feature columns\n\t%s" % '\n\t'.join(shared_headers))  

  print("Done.\n")
