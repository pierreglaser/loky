import datetime
import os
import importlib
import itertools
import json
import time
import sys


import loky


import benchmarks

N_ITER = 5
LOKY_PICKLERS = ['dill', 'cloudpickle', 'pickle']

# get benchmark directory to later store the results here
benchmarks_dir = os.path.dirname(__file__)

# Get the commit hash of loky's current head
repo_path = os.path.dirname(loky.__file__)
commit_hash = os.popen(
        'git -C {} rev-parse --short HEAD'.format(repo_path)).read()

# Remove the \n at the end of the os.popen output
commit_hash = commit_hash.split()[0]

LOKY_PICKLER = os.environ.get('LOKY_PICKLER')
if LOKY_PICKLER is None:
    raise ValueError('LOKY_PICKLER environment variable should be set')

CURRENT_DATE = datetime.date.today().isoformat()


def save(result, path):

    if os.path.exists(path):
        # append previous result to existing results. This may become slow
        # if the results file increases in size
        with open(path, 'r+') as f:
            previous_results = json.load(f)
    else:
        previous_results = []

    previous_results.append(result)

    with open(path, 'w') as f:
        json.dump(previous_results, f)


def benchmark(func_name, metadata, path):
    func = getattr(benchmarks, func_name)
    if func is None:
        raise ValueError('func_name could not be found in benchmark file')

    # j = 0
    for params in itertools.product(*func.params):
        # j += 1
        # if j > 2:
        #     break
        running_times = []
        print('running with params {}'.format(params))

        for i in range(N_ITER):
            start_time = time.time()
            func(*params)
            running_time = time.time() - start_time
            running_times.append({'iter_no': i, 'time': running_time})

        result = {'times': running_times,
                  **metadata,
                  **dict(zip(func.param_names, params))}
        save(result, path)
    return running_times


if __name__ == "__main__":
    for bench_name in benchmarks.ALL_BENCHMARKS:
        print('benchmarking {} with {}...'.format(bench_name, LOKY_PICKLER))
        path = os.path.join(benchmarks_dir, 'results',
                            '{}.json'.format(bench_name))

        metadata = {'commit': commit_hash, 'pickler': LOKY_PICKLER,
                    'date': CURRENT_DATE, 'name': bench_name}
        running_times = benchmark(bench_name, metadata, path)
