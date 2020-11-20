

MOCK_DIR=$1

if [[ -z $MOCK_DIR ]]; then
  echo "usage: ./create_dir.sh /DIR/TO/MOCK"
  exit 1
fi 

DIRS=$(find $MOCK_DIR -type d | sed "s:${MOCK_DIR}:.:g")
FILES=$(find $MOCK_DIR -type f | sed "s:${MOCK_DIR}:.:g")

for dir in $DIRS; do
  mkdir -p ${dir}
done

for file in $FILES; do
  touch $file
done


