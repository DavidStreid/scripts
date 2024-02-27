
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
