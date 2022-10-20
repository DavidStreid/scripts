
# Run
## Defaults
```
$ ./install_python.sh 3.9.15
[CONFIG]
	python_version=3.9.15
	ssl_dir=
	tgt_dir=
	Installing python3.9.15 to default location
wget https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz
	SUCCESS
tar -xzvf Python-3.9.15.tgz
	SUCCESS
cd Python-3.9.15 && ./configure --enable-optimizations
	SUCCESS
make altinstall
	SUCCESS
```

## options
### specify openssl
* Needed for some linux distros that use unsupported ssl version and require a manual installation of a newer `openssl`
  * e.g. centos7 noted in [github issues](https://github.com/pypa/pip/issues/10939) & [python bugs](https://bugs.python.org/issue47201)

```
$ ./install_python.sh 3.9.15 /usr/local/openssl /usr/local/bin/
[CONFIG]
	python_version=3.9.15
	ssl_dir=/usr/local/openssl
	tgt_dir=/usr/local/bin/
wget https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz
	SUCCESS
tar -xzvf Python-3.9.15.tgz
	SUCCESS
cd Python-3.9.15 && ./configure --enable-optimizations --with-openssl=/usr/local/openssl --prefix=/usr/local/bin/
	SUCCESS
make altinstall
	SUCCESS
```
