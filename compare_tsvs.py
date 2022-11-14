#!/usr/local/bin/python3
import sys

def main():
  f1 = sys.argv[1]
  f2 = sys.argv[2]
  key = sys.argv[3]
  delimiter = '\t'

  print("INPUTS")
  print(f"\td1: Dictionary for {f1}")
  print(f"\td2: Dictionary for {f2}")
  print(f"\tDIFF_KEY={key}")

  d1 = read_file(f1, key, delimiter)
  d2 = read_file(f2, key, delimiter)

  shared_keys, only_d1_keys, only_d2_keys, diffs = get_keys(d1, d2)
  key_diffs = compare_shared_keys(shared_keys, d1, d2)

  total_diffs = diffs + key_diffs
  if len(total_diffs) == 0:
    print("TSVs are same")
  else:
    print("TSVs are different")
    print("DIFFS")
    print("\t" + "\n\t".join(total_diffs))


def compare_shared_keys(shared_keys, d1, d2):
  print("SHARED_KEYS_STATUS")
  same, diff = 0, 0
  key_diffs = []
  for k in shared_keys:
    e1 = d1[k]
    e2 = d2[k]

    if e1 != e2:
      diff += 1
      key_diffs.append(f"KEY={k}")
    else:
      same += 1

  print(f"\tSAME={same}\tDIFF={diff}")

  return key_diffs


def parse(raw_line, delimiter):
  return raw_line.strip().split(delimiter)


def read_file(fname, key, delimiter):
  dic = {}
  with open(fname, 'r') as in_f:
    header = parse(in_f.readline(), delimiter)
    for line in in_f:
      vals = parse(line, delimiter)
      entry = dict(zip(header, vals))
      k = entry[key]
      dic[k] = entry
  return dic
  

def get_keys(d1, d2):
  shared = list(set(d1.keys()).intersection(set(d2.keys())))
  only_1 = list(set(d1.keys()).difference(set(d2.keys())))
  only_2 = list(set(d2.keys()).difference(set(d1.keys())))

  num_unique_d1 = len(shared) + len(only_1)
  num_unique_d2 = len(shared) + len(only_2)

  total_d1 = len(d1)
  total_d2 = len(d2)
  diffs = []
  if total_d1 != num_unique_d1:
    diffs.append(f"[WARN] d1 has non-unique entries\tTOTAL={total_d1}\tUNIQUE={num_unique_d1}")
  if total_d2 != num_unique_d2:
    diffs.append(f"[WARN] d1 has non-unique entries\tTOTAL={total_d2}\tUNIQUE={num_unique_d2}")

  return shared, only_1, only_2, diffs



if __name__ == '__main__':
  main()