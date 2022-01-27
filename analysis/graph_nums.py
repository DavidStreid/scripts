import sys
import matplotlib.pyplot as plt

DELIMITER = ","


def graph_scatter(list_of_nums, title):
  idx_list = [ idx for idx in range(len(list_of_nums)) ]
  plt.scatter(idx_list, list_of_nums)
  plt.title(title)
  plt.xlabel('idx')
  plt.ylabel('val')
  fname = "%s___%s" % ("_".join(title.split(" ")), "scatter")
  plt.savefig("%s.pdf" % fname)
  plt.close()


def graph_scatter_aggregate(list_of_nums, title):
  round_to = 3
  rounded = [ round(val, round_to) for val in list_of_nums ]
  counted_dic = {}
  for val in rounded:
    if val in counted_dic:
      counted_dic[val] += 1
    else:
      counted_dic[val] = 1
  x = []
  y = []
  for val, ct in counted_dic.items():
    x.append(val)
    y.append(ct)
  plt.scatter(x, y)
  plt.title(title)
  plt.xlabel('val')
  plt.ylabel('ct')
  fname = "%s___%s" % ("_".join(title.split(" ")), "scatter_aggregate")
  plt.savefig("%s.pdf" % fname)
  plt.close()


def graph_hist(list_of_nums, title):
  '''Creates histogram
  :param list_of_nums, float[]
  :param title, str
  '''
  num_bins = 10
  plt.hist(list_of_nums, num_bins, facecolor='blue', alpha=0.5)
  plt.title(title)
  plt.xlabel('My numbers')
  plt.ylabel('Count')   
  fname = "%s___%s" % ("_".join(title.split(" ")), "hist")
  plt.savefig("%s.pdf" % fname)
  plt.close()


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

  header_vals_list = []
  for col_vals in list_of_col_values:
    headers = [ val for val in col_vals if not is_float(val) ]
    if len(headers) == 1:
      header = headers[0]
    else:
      header = None
    if len(headers) == len(col_vals):
      print("\t\tIgnoring column: '%s'" % headers[0])
      # Skip any columns w/ just words
      continue
    
    vals = [ float(val) for val in col_vals if is_float(val) ]
    
    header_vals_list.append( [ header, vals ] ) 

  return header_vals_list

def is_float(element: any) -> bool:
    # https://stackoverflow.com/a/20929881/3874247
    try:
        float(element)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Pass a file. Exiting...")
    sys.exit(1)

  summary_file = sys.argv[1]
  print("Input=%s" % summary_file)

  print("\tProcessing...")
  header_vals_list = get_columns(summary_file)

  print("\tGraphing...")
  for header_vals in header_vals_list:
    title = header_vals[0]
    list_of_nums = header_vals[1]
   
    graph_hist(list_of_nums, title)
    graph_scatter(list_of_nums, title)
    graph_scatter_aggregate(list_of_nums, title)

  print("Done.")
