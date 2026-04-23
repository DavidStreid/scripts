
# Decorator to log fucntions
```
def log_fn(func):
  def wrapper(*args, **kwargs):
      args_to_print = ', '.join([a if type(a) in {int, float, str, bool} else a.__class__.__name__ for a in args])
      print(f'{func.__name__}({args_to_print})')
      return func(*args, **kwargs)
  return wrapper
```

Can be used as follows
```
@log_fn
def tester(arg1, arg2):
  pass
tester("hello", "world")
```
Will print
```
tester("hello", "world")
```

# Setup
| RPM-based, yum (CentOS/Fedora/RH) | Debian-based, apt (Ubuntu) | Purpose                                                                                                 |
|-----------------------------------|----------------------------|---------------------------------------------------------------------------------------------------------|
| python-devel                      | python-dev                 | provide development headers and libraries necessary for compiling and building Python extension modules |

```
yum -y install pip python-devel
apt install python3.10-dev
```

# `uv`
tool for managing python environments

## Quick runbook

Individual script
* why? Creates a self-contained environment so anyone can run this script and get the same results

```
uv init --script my_script.py
uv lock --script my_script.py
```

For Adding packages, use `uv add`, which will automatically update the `.py.lock` file
```
uv add --script my_script.py requests
```

e.g. After all three commands below
```
$ ls
my_script.py            my_script.py.lock
$ head -5 my_script.py
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.32.5",
# ]
```

# Libraries

## tqdm

Quick progress bar for for-loops & iterables

```
from tqdm import tqdm
import time
ct = 100
for i in tqdm(range(100), desc="count", leave=False, total=ct):
  time.sleep(0.01)
```

**OUTPUT**
```
count:  45%|███████        | 45/100 [00:01<00:00, 81.58it/s]
# if leave=False, this bar will disappear when it completes
```
