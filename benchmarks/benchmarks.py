import os
import numpy as np


from loky.process_executor import ProcessPoolExecutor


def dummy_func(*args, **kwargs):
    return args


def make_data(data_structure, size):
    if data_structure == 'list':
        return list(range(size))
    elif data_structure == 'dict':
        return dict(zip(range(size), range(size)))
    elif data_structure == 'bytes':
        return os.urandom(size)
    elif data_structure == 'array':
        return np.arange(size)
    else:
        raise ValueError('data structure {} not understood'.format(
            data_structure))


def get_task(task):
    if task == 'dummy':
        return dummy_func
    else:
        raise ValueError('task {} not recognized'.format(task))


def get_pickle_module(pickler):
    if pickler == 'pickle':
        import python_pickle as pickle
    elif pickler == 'cpickle':
        import pickle
    elif pickler == 'cloudpickle':
        import cloudpickle as pickle
    else:
        raise ValueError('pickler {} not understood'.format(
            imlementation))
    return pickle


def send_tasks(data_structure, size, task, n_tasks, max_workers):
    data = make_data(data_structure, size)
    fn = get_task(task)
    executor = ProcessPoolExecutor(max_workers=max_workers)
    for r in executor.map(fn, [data for _ in range(n_tasks)]):
        pass


send_tasks.param_names = ['data_structure', 'size', 'task',
                          'n_tasks', 'max_workers']
send_tasks.params = (
        ['list', 'dict', 'bytes', 'array'],
        [1000, 10000, 100000],
        ['dummy'],
        [10, 100, 300],
        [2])


def pickle_depickle(data_structure, size, pickler):
    data = make_data(data_structure, size)
    pickle_module = get_pickle_module(pickler)
    pickle_module.loads(pickle_module.dumps(data))


pickle_depickle.param_names = ['data_structure', 'size', 'pickler']
pickle_depickle.params = (
        ['list', 'dict', 'bytes', 'array'],
        [1000, 10000, 100000],
        ['cpickle', 'pickle', 'cloudpickle'],
        )


ALL_BENCHMARKS = ['send_tasks', 'pickle_depickle'][:1]
