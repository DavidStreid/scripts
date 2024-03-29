import sys
from os.path import exists
from scipy import stats
import matplotlib.pyplot as plt
import math
import argparse
import numpy as np

DEFAULT_DELIMITER = ","

def graph_scatter(x_axis, y_axis, x_label, y_label, fname):
  plt.scatter(x_axis, y_axis)
  plt.title('%s vs. %s' % (y_label, x_label))
  plt.xlabel(x_label)
  plt.ylabel(y_label)

  plt.savefig("%s.pdf" % fname)
  plt.close()


def graph_scatter_with_idx(list_of_nums, title):
  idx_list = [ idx for idx in range(len(list_of_nums)) ]
  fname = "%s___%s" % ("_".join(title.split(" ")), "scatter")
  graph_scatter(idx_list, list_of_nums, 'idx', title, fname)


def graph_scatter_count(list_of_nums, title):
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

  fname = "%s___%s" % ("_".join(title.split(" ")), "scatter_aggregate")
  graph_scatter(x, y, title, 'count', fname)


def graph_scatter_count_nl(list_of_nums, title):
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
  skipped_zero = None
  for val, ct in counted_dic.items():
    if val != 0:
      x.append(math.log(val))
      y.append(ct)
    else:
      skipped_zero = ct
  if skipped_zero is not None:
    print(f"\t\tSkipped {skipped_zero} '0' values")
  fname = "%s___%s" % ("_".join(title.split(" ")), "scatter_aggregate_nat_log")
  graph_scatter(x, y, f'{title} (ln)', 'count', fname)


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


def get_columns(f_name, delimiter):
  cols = []
  with open(f_name, 'r') as summary_in:
    for line in summary_in:
      cleaned = line.strip()
      vals = [ v.strip() for v in cleaned.split(delimiter) ]
      cols.append(vals)

  if len(cols) == 0:
    print("ERROR - empty file")
    sys.exit(1)

  num_cols_list = list(set([ len(vals) for vals in cols ]))
  if len(num_cols_list) > 1:
    num_columns_to_analyze = min(list(num_cols_list))
    print(f"WARNING - some columns are missing values. Only analyzing first {num_columns_to_analyze} columns")
  num_cols = sorted(num_cols_list)[0]

  list_of_col_values = []
  for col_idx in range(num_cols):
    l = [ line[col_idx] for line in cols ]
    list_of_col_values.append(l)

  header_vals_list = []
  for col_vals in list_of_col_values:
    headers = [ val for val in col_vals if not is_float(val) ]

    if len(headers) == len(col_vals):
      print("\tIgnoring non-numeric column='%s'" % headers[0])
      continue
    if len(headers) > 0:
      header = headers[0]
      if len(headers) > 1:
        header_options=[f"'{val}'" for val in headers]
        print("\tIgnoring non-numeric column='%s'" % headers[0])
        # invalid_indices=[]
        # for idx, col in enumerate(col_vals):
        #   if col in headers[1:]:
        #     invalid_indices.append(idx)
        # for idx, line in enumerate(cols):
        #   if idx in invalid_indices:
        #     print(f"\t{delimiter.join(line)}")
        continue
    else:
      header = None

    if header is not None:
      print("\tProcessing column=%s" % header)

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


def add_to_bin(bin, idx, bar_y_values, bar_x_values, bin_x_mapping, bins):
  ''' Util for @graph_bar_with_averages '''
  bin_name = f"b{idx+1}"
  x_vals = [ tup[0] for tup in bin ]
  y_vals = [ tup[1] for tup in bin ]
  y_avg = sum(y_vals) / len(y_vals)
  bar_y_values.append(y_avg)
  bar_x_values.append(bin_name)
  bin_x_mapping.append([bin_name, min(x_vals), max(x_vals), len(x_vals), y_avg])
  bins.append(bin)

def graph_bar_with_averages(x_vals, y_vals, x_axis, y_axis, fname):
  ''' With multiple datapoints, simplifies by grouping x_values and reporting their average as the y'''
  assert len(x_vals) == len(y_vals)

  tuples = list(zip(x_vals, y_vals))
  tuples.sort(key=lambda tup: tup[0])

  bar_x_values = []
  bar_y_values = []
  bin_x_mapping = []
  bin_size = int(len(x_vals) / 10) + 1
  bins = []
  bin = []
  for idx, tup in enumerate(tuples):
    bin.append(tup)
    if (idx + 1) % bin_size == 0:
      add_to_bin(bin, len(bins), bar_y_values, bar_x_values, bin_x_mapping, bins)
      bin = []
  if len(bin) > 0:
    add_to_bin(bin, len(bins), bar_y_values, bar_x_values, bin_x_mapping, bins)

  with open(f"bin_info_{fname}.tsv", "w") as bin_info_out:
    bin_info_out.write("bin_name\tbin_min\tbin_max\tnum\tavg_y\n")
    for row in bin_x_mapping:
      bin_info_out.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n")

  bar_x_indices = np.arange(len(bar_x_values))

  plt.bar(bar_x_indices, bar_y_values, align='center', alpha=0.5)
  plt.xticks(bar_x_indices, bar_x_values)
  plt.xlabel(x_axis)
  plt.ylabel(y_axis)
  plt.title(fname)
  plt.savefig("%s.pdf" % fname)
  plt.close()


def graph_selected_axes(x_axis, y_axis, header_vals_list, x_min, x_max):
  x_vals, y_vals = None, None

  for header_vals in header_vals_list:
    if header_vals[0] == x_axis:
      x_vals = header_vals[1]
    elif header_vals[0] == y_axis:
      y_vals = header_vals[1]
      
  if not x_vals or not y_vals:
    print("\t\t[ERROR] Invalid - x_axis=%s y_axis=%s" % (x_axis, y_axis))
  else:
    if x_min is not None or x_max is not None:
      filter_label = ''
      if x_min is None:
        x_min = float("-inf")
      else:
        filter_label = f"xmin{x_min}"
        x_min = float(x_min)
        print(f"\t\tmin_x_filter={x_min}")
      if x_max is None:
        x_max = float("inf")
      else:
        if filter_label == '':
          filter_label = f"xmax{x_max}"
        else:
          filter_label = f"{filter_label}_xmax{x_max}"
        x_max = float(x_max)
        print(f"\t\tmax_x_filter={x_max}")

      filtered_indices = []
      for idx, x_val in enumerate(x_vals):
        if x_val > x_min and x_val < x_max:
          filtered_indices.append(idx)

      filtered_x_vals = []
      for idx, x_val in enumerate(x_vals):
        if idx in filtered_indices:
          filtered_x_vals.append(x_val)
      filtered_y_vals = []
      for idx, y_val in enumerate(y_vals):
        if idx in filtered_indices:
          filtered_y_vals.append(y_val)

      print(f"\t\tFiltered n={len(filtered_indices)} from n={len(x_vals)}")
      x_vals = filtered_x_vals
      y_vals = filtered_y_vals

      
      print(f"\t\tMEAN_{y_axis}={sum(y_vals)/len(y_vals)} (n={len(y_vals)})")
      print(f"\t\tMEAN_{x_axis}={sum(x_vals)/len(x_vals)} (n={len(x_vals)})")
      print(f"\t\tMIN_{y_axis}={min(y_vals)}")
      print(f"\t\tMAX_{y_axis}={max(y_vals)}")
      fname = '%s_vs_%s___F%s' % (y_axis, x_axis, filter_label)
    else:
      fname = '%s_vs_%s' % (y_axis, x_axis)
    if len(set(x_vals)) == 1 or len(set(y_vals)) == 1:
      print(f"(0) Pearson’s correlation coefficient: n/a (x={x_axis} y={y_axis})") 
    else:
      (pearson_correlation_coefficient, pvalue) = stats.pearsonr(x_vals, y_vals) # e.g. (-0.7426106572325057, 0.1505558088534455)

      m, c = np.polyfit(x_vals, y_vals, 1)
      print(f"\tLeast squares polynomial fit: y = {m}x + {c}")
      slope = '(-)' if pearson_correlation_coefficient < 0 else '(+)'
      print(f"\tPearson’s correlation coefficient {slope}: {pearson_correlation_coefficient} (x={x_axis} y={y_axis})")

    graph_scatter(x_vals, y_vals, x_axis, y_axis, fname)

    bar_fname = f'bar_{fname}'
    graph_bar_with_averages(x_vals, y_vals, x_axis, y_axis, bar_fname)


def validate_inputs(summary_file, x_axis, y_axis, columns, all_headers_set):
  errors = []
  if not exists(summary_file):
    errors.append(f'Invalid csv: {summary_file}')
  if (x_axis or y_axis) and not (x_axis and y_axis):
    errors.append(f'Both x & y columns need to be provided to comare: x="{x_axis}" y="{y_axis}"')
  if columns:
    for column in columns:
      if column not in all_headers_set:
        errors.append(f'column={column} is not in the header of the csv')

  if len(errors) > 0:
    print("ERRORS")
    for err in errors:
      print(f'\t{err}')
    sys.exit(1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Graph CSV file')
  parser.add_argument('-f', dest='input_file', help='comma-separated file', required=True)
  parser.add_argument('-x', dest='x_axis', help='x_axis column (must provide -y)', default=None)
  parser.add_argument('-y', dest='y_axis', help='y_axis column (must provide -x)', default=None)
  parser.add_argument('-c', dest='columns', help='space-delimited string of columns to graph (e.g. -c "c1 c2")', default=None)
  parser.add_argument('-d', dest='delimiter', help='delimiter for input_file (-f). Default: ","', default=DEFAULT_DELIMITER)
  parser.add_argument('-xmin', dest='xmin', help='minimum x value to include in correlation', default=None)
  parser.add_argument('-xmax', dest='xmax', help='maximum x value to include in correlation', default=None)

  args = parser.parse_args()
  summary_file = args.input_file
  x_axis = args.x_axis
  y_axis = args.y_axis
  columns = args.columns
  delimiter = args.delimiter
  
  x_min = args.xmin
  x_max = args.xmax

  print("Inputs")
  print(f"\tcsv={summary_file} (delimiter={delimiter})")

  if delimiter == "\\t":
    delimiter = "\t"
  if x_axis:
    print(f"\tx='{x_axis}'")
  if y_axis:
    print(f"\ty='{y_axis}'")
  if columns:
    print(f"\tcolumms='{columns}'")
    columns = columns.strip().split(" ")
  else:
    print("\tcolumns=[all]")


  print("Processing...")
  header_vals_list = get_columns(summary_file, delimiter)
  all_headers = set([hv[0] for hv in header_vals_list])
  validate_inputs(summary_file, x_axis, y_axis, columns, all_headers)

  print("Graphing...")
  if x_axis and y_axis:
    print("\t[graph] %s vs %s..." % (x_axis, y_axis))
    graph_selected_axes(x_axis, y_axis, header_vals_list, x_min, x_max)
  else:
    for header_vals in header_vals_list:
      if columns:
        if header_vals[0] not in columns:
          continue
      
      column = header_vals[0]
      list_of_nums = header_vals[1]
      print(f"\t[graph] {column}")
      num_vals = len(list_of_nums)

      title = f'{column}_n{num_vals}'

      graph_hist(list_of_nums, title)
      graph_scatter_with_idx(list_of_nums, title)
      graph_scatter_count(list_of_nums, title)
      graph_scatter_count_nl(list_of_nums, title)


  print("Done.")
