
# Run
## Defaults
```
$ ./install_python.sh -v 3.9.15
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
`-s` string
  > Eg: `/usr/local/openssl`

Directory of custom SSL library (See **Troubleshooting** for more info)

`-t` string
  > E.g. `/usr/local/bin`

Directory to install python version to


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

# Troubleshooting
## openssl
**Description**: When installing requirements of python after installing, `pip` might not have built the required (but oddly optional in that the python install will succeed) `ssl` module. When doing a `pip install`, an error like this might be logged -

    WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
    WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/jinja2/
    ...

And if looking at the logs of the `make altinstall` step, there may be one of these lines -

**python v3.10+**

    Could not build the ssl module!
    Python requires a OpenSSL 1.1.1 or newer

**python v3.9 and below**

    Python requires an OpenSSL 1.0.2 or 1.1 compatible libssl with X509_VERIFY_PARAM_set1_host()

Solution: **python requires compatible openssl to install dependencies**

### Solution - Install python packages that pull required system library header files 
Try to install the dependencies ([REF](https://devguide.python.org/getting-started/setup-building/index.html#linux)) required by python to obtain the right system library headers, such as the headers for `openssl`. Since this is packaged w/ the OS distribution, they might not be easily found, or not be present.

e.g. for yum-like systems. See link for other OS's

    sudo yum install yum-utils
    sudo yum-builddep python3

### Solution - Custom SSL library (`./install_python <VERSION> -ssl_dir <OPENSSL_DIR>`)
* Use this when building a custom SSL library, i.e. not using the `openssl` packaged w/ the os distribution. If doing this, the directory `OPENSSL_DIR` should have the subdirecotries `lib` & `certs`.
  * Seen in coummunity linux distributions
    * e.g. centos7 comes w/ `openssl 1.0.2,`, which was EOL in 2019 - anything python version 3.10 and above will fail since later versions of python require a minimum `openssl` version of `1.1.1` 
      * [github issues](https://github.com/pypa/pip/issues/10939)
      * [python bugs](https://bugs.python.org/issue47201)
