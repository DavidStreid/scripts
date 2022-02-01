from os import X_OK
import sys
from sklearn.neighbors import KNeighborsClassifier

DELIMITER = ','

def train_knn(x, y):
  # x = [[0], [1], [2], [3]]
  # y = [0,0,1,1]
  neigh = KNeighborsClassifier(n_neighbors=3)
  neigh.fit(x, y)

  return neigh



def  get_columns(f_name):
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

  header_vals_list = []
  for col_vals in list_of_col_values:
    headers = [ val for val in col_vals if not is_float(val) ]
    if len(headers) == 1:
      header = headers[0]
    else:
      header = None
    if len(headers) == len(col_vals):
      # Skip any columns w/ just words
      continue
    
    vals = [ float(val) for val in col_vals if is_float(val) ]
    header_vals_list.append( [ header, vals ] ) 

  val_len = set([ len(line[1]) for line in header_vals_list ])
  if len(val_len) != 1:
    print("\t[ERROR] - Invalid value columns")
    sys.exit(1)

  return header_vals_list, list(val_len)[0]

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

def write_cols_to_file(header_vals_list):
  with open('predictions.csv', 'w') as out:
    header = [ col[0] for col in header_vals_list ]
    values = [ col[1] for col in header_vals_list ]

    all_col_lengths = list(set([len(col_vals) for col_vals in values]))
    if len(all_col_lengths) != 1:
      print("[WARNING] Invalid number of input values - [ %s ]" % ', '.join([str(val) for val in all_col_lengths]))

    out.write(f"{','.join(header)}\n")
    for i in range(all_col_lengths[0]):
      line = f"{','.join([ str(value[i]) for value in values ])}\n"
      out.write(line)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Pass a file. Exiting...")
    sys.exit(1)

  training_file = sys.argv[1]
  test_file = sys.argv[2]

  category = None
  features = None

  print("inputs")
  print("\tfile: %s" % training_file)
  if len(sys.argv) > 4:
    category = sys.argv[3]
    features = sys.argv[4:]
    print("\tcategory: %s" % category)
    print("\tfeatures (num=%s): [ %s ]" % (len(features), ', '.join(features)))

  header_vals_list, num_vals = get_columns(training_file)
  test_header_vals_list, test_num_vals = get_columns(test_file)

  if category and features:
    print("Training...")
    category_idx, features_idx = get_feature_and_category_indices(header_vals_list, category, features)
    x, y = get_x_and_y(header_vals_list, num_vals, features_idx, category_idx)
    knn_model = train_knn(x, y)

    print("Testing")
    features_idx = get_feature_indices(test_header_vals_list, features)
    x_test = get_x(test_header_vals_list, test_num_vals, features_idx)

    
    predictions = []
    prediction_report = {}
    for x_t in x_test:
      prediction = knn_model.predict([x_t])
      prediction_label = prediction[0]
      predictions.append(prediction_label)

      if prediction_label in prediction_report:
        prediction_report[prediction_label] += 1
      else:
        prediction_report[prediction_label] = 1

    print(f"Classifications (n={len(x_test)})")
    for k,v in prediction_report.items():
      print(f'\t{k}: {v}')

    prediction_col = ['prediction', predictions]
    test_header_vals_list.append(prediction_col)
    write_cols_to_file(test_header_vals_list)
  else:
    all_headers = [ val[0] for val in header_vals_list ]
    print("Possible feature columns\n\t%s" % '\n\t'.join(all_headers))

  print("Done.")