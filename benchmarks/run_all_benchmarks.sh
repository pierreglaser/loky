set -u
LOKY_PICKLERS=(cloudpickle pickle)

for pickler in ${LOKY_PICKLERS[*]};
do
   echo "running benchmarks for pickler=$pickler"
   LOKY_PICKLER=$pickler python benchmark.py
done

