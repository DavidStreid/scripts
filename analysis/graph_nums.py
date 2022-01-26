import matplotlib.pyplot as plt

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
