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
      print("\t[ERROR] Invalid category column: %s" % category)
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

def run_predictions(x, y, x_test):
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

    print(f"\t[{model_label}] Classifications (n={len(x_test)})")
    for k,v in prediction_report.items():
      print(f'\t\t{k}: {v}')

    prediction_col = [model_label, predictions]
    prediction_list.append(prediction_col)

  return prediction_list

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Pass a file. Exiting...")
    sys.exit(1)

  training_file = sys.argv[1]
  test_file = sys.argv[2]

  category = None
  features = None

  print("Inputs")
  print("\tfile: %s" % training_file)
  if len(sys.argv) > 4:
    category = sys.argv[3]
    features = sys.argv[4:]
    print("\tcategory: %s" % category)
    print("\tfeatures (num=%s): [ %s ]" % (len(features), ', '.join(features)))

  numerical_column_list, categorical_column_list, num_vals = get_columns(training_file)
  test_numerical_column_list, test_categorical_column_list, test_num_vals = get_columns(test_file)

  if category and features:
    out_file = f"{category}_predictions___{'_'.join(features)}.csv"
    print("Training...")
    category_idx, features_idx = get_feature_and_category_indices(numerical_column_list, category, features)
    x, y = get_x_and_y(numerical_column_list, num_vals, features_idx, category_idx)

    print("Extracting test set...")
    features_idx = get_feature_indices(test_numerical_column_list, features)
    x_test = get_x(test_numerical_column_list, test_num_vals, features_idx)

    print("Running classifiers...")
    prediction_list = run_predictions(x, y, x_test)



    write_cols_to_file(test_categorical_column_list, test_numerical_column_list, prediction_list, out_file)

  else:
    # If only two files are passed - just get the columns that could be features/categories
    all_headers = [ val[0] for val in numerical_column_list ]
    print("Possible feature columns\n\t%s" % '\n\t'.join(all_headers))

  print("Done.\n")
