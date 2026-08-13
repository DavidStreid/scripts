
# Logging

## Decorator to log fucntions
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

## Simple update to add metadata to logging

1. Add logging config

  ```
  import logging
  
  # Configure logging at the start of your script
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
  )
  ```

2. Ctrl-R `"print("` -> `"logging.info("`

# StackTrace
```
def stacktrace():
    frames = []
    try:
        frame = sys._getframe(1)  # Get the frame AFTER _get_caller_info
        while frame:
            filename = frame.f_code.co_filename
            base_file = os.path.basename(filename)
            func_name = frame.f_code.co_name
            frames.append(f"{base_file}::{func_name}")
            frame = frame.f_back
    except Exception:
        pass

    if not frames:
        return "Unknown"

    frames.reverse()  # Order from root to caller
    return " > ".join(frames)
```

**OUTPUTS**

```
main.py::<module> > tsak.py::process_data > runner.py::execute_step
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

## run unbuffered

Achieving the same thing as `python -u ...`

```
PYTHONUNBUFFERED=1 uv run my_script.py 2>&1 | tee log_my_script.out
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

## [`shiv`](https://github.com/linkedin/shiv)

Creates binaries of python packages
* WARNING - zipapps created with shiv will extract themselves into `~/.shiv`, unless overridden via `SHIV_ROOT`, i.e. there may be runtime issues of multiple users

```
$ shiv -c flake8 -o ~/bin/flake8 flake8
$ ~/bin/flake8 --version
3.7.8 (mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.7.4 on Darwin
```

For hard-to-resolve dependencies, install dependencies to a separate virtual env and use that,
```
./dep_env/python -m pip install -r requirements.txt
./dep_env/python -m pip install .

shiv --python python3.12 --site-packages ./dep_env/lib64/python3.9/site-package -o ~/bin/my_lib -c my_lib
```

# DEV libraries

## Parallelize

* `concurrent.futures` - asynchronous execution providing the following executors -
  * `ProcessPoolExecutor` - separate memory & python executor [CPU-bound]
  * `ThreadPoolExecutor` - lightweight, shared memory [I/O-bound]

NOTE - The instance of `ThreadPoolExecutor` or `ProcessPoolExecutor` parallelizes via a `executor.map` function, that only operates on one input at a time. To add additional inputs, use `functools::partial`, e.g.

  ```
  worker_fn = partial(_process_tsv_line, headers=headers)
  executor.map(worker_fn, entries)
  ```

```
from concurrent.futures import ProcessPoolExecutor
import time

def compute_square(n: int) -> int:
  time.sleep(0.5)
  return n * n

if __name__ == "__main__":
  print("Starting parallel processing...")
  numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  start_time = time.time()
  with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute_square, numbers))
  end_time = time.time()
  print(f"Results: {results}")
  print(f"Completed in {end_time - start_time:.2f} seconds.")
```
