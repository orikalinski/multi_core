import time

SECOND_TO_MICROSECONDS = 1000000

method_to_pretty_name = {'merge_sort_multi_processed': 'MergeSort'}


def timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        print('%s: %2.5f' % (method_to_pretty_name.get(method.__name__, method.__name__),
                             (te - ts) * SECOND_TO_MICROSECONDS))
        return result

    return timed


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def read_file(file_path):
    with open(file_path, "r") as f:
        return [int(a) for a in f.readlines()]


def handle_processes(processes):
    for process in processes:
        process.start()

    for process in processes:
        process.join()
