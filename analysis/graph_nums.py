import sys
import matplotlib.pyplot as plt

DELIMITER = ","

def graph(list_of_nums, title):
  '''Creates bar graph
  :param list_of_nums, float[]
  :param title, str
  '''
  num_bins = 10
  plt.hist(list_of_nums, num_bins, facecolor='blue', alpha=0.5)
  plt.title(title)
  plt.xlabel('My numbers')
  plt.ylabel('Count')   
  fname = "_".join(title.split(" "))
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
  if len(num_cols_list) > 0:
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
    
    vals = [ val for val in col_vals if is_float(val) ]
    
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
  '''
  input_file example
    mean,median,std
    0.4814276023050369,0.4878048780487805,0.1284245675290927
  '''
  if len(sys.argv) < 2:
    print("Pass a file like below (Headers optional). Exiting...\n")
    print("$ cat my_file.txt")
    print("mean,median,std")
    print("0.4814276023050369,0.4878048780487805,0.1284245675290927")
    sys.exit(1)

  summary_file = sys.argv[1]
  header_vals_list = get_columns(summary_file)
  for header_vals in header_vals_list:
    title = header_vals[0]
    list_of_nums = header_vals[1]
   
    graph(list_of_nums, title)
