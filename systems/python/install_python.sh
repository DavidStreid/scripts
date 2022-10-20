PYTHON_VERSION=$1
ssl_dir=$2
tgt_dir=$3

CMD_LOG=$(pwd)/log_run_cmd.out

run_cmd() {
  CMD=$@
  echo ${CMD}
  eval ${CMD} > ${CMD_LOG} 2>&1
  if [[ $? -eq 0 ]]; then
    printf "\tSUCCESS\n"
  else
    printf "\tFAILED\n"
    exit 1
  fi
}



echo "[CONFIG]"
printf "\tpython_version=${PYTHON_VERSION}\n"
printf "\tssl_dir=${ssl_dir}\n"
printf "\ttgt_dir=${tgt_dir}\n"

DNLD="wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"
EXCT="tar -xzvf Python-${PYTHON_VERSION}.tgz"
CONF="cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations"
if [[ ! -z ${ssl_dir} ]]; then
  CONF+=" --with-openssl=${ssl_dir}"
fi
if [[ ! -z ${tgt_dir} ]]; then
  CONF+=" --prefix=${tgt_dir}"
else
  printf "\tInstalling python${PYTHON_VERSION} to default location\n"
fi

# MAKE="make && make test"
INST="make altinstall"

run_cmd ${DNLD}
run_cmd ${EXCT} && \
run_cmd ${CONF} && \
run_cmd ${INST}

