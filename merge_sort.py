import math
import multiprocessing

from utils import timeit, chunks, handle_processes, read_file


class MergeSort(object):
    @timeit
    def merge_sort_multi_processed(self, items, num_of_processes=multiprocessing.cpu_count()):
        manager = multiprocessing.Manager()
        sorted_chunks = manager.dict()
        processes = list()
        chunk_size = int(math.ceil(len(items) / num_of_processes))
        for i, items_subset in enumerate(chunks(items, chunk_size)):
            processes.append(multiprocessing.Process(target=self.__merge_sort_single_processed_wrapper,
                                                     args=(items_subset, sorted_chunks, i)))

        handle_processes(processes)
        return self.__merge_list_of_sorted_items(sorted_chunks.values())

    @timeit
    def merge_sort_single_processed(self, items):
        return self.__merge_sort_single_processed_rec(items)

    def __merge_sort_single_processed_wrapper(self, items, results_dict, process_number):
        results_dict[process_number] = self.__merge_sort_single_processed_rec(items)

    def __merge_sort_single_processed_rec(self, items):
        items_length = len(items)
        if items_length <= 1:
            return items
        middle = items_length // 2
        sorted_left_items = self.__merge_sort_single_processed_rec(items[:middle])
        sorted_right_items = self.__merge_sort_single_processed_rec(items[middle:])
        return self.__merge(sorted_left_items, sorted_right_items)

    def __merge_wrapper(self, left_items, right_items, results_dict, process_number):
        results_dict[process_number] = self.__merge(left_items, right_items)

    def __merge(self, left_items, right_items):
        merged_list = list()
        i, j = 0, 0
        left_len, right_len = len(left_items), len(right_items)
        while i < left_len and j < right_len:
            if left_items[i] < right_items[j]:
                merged_list.append(left_items[i])
                i += 1
            else:
                merged_list.append(right_items[j])
                j += 1
        merged_list.extend(left_items[i:])
        merged_list.extend(right_items[j:])
        return merged_list

    def __merge_list_of_sorted_items(self, list_of_sorted_items):
        manager = multiprocessing.Manager()
        while len(list_of_sorted_items) > 2:
            processes = list()
            merged_chunks = manager.dict()
            for i, two_chunks in enumerate(chunks(list_of_sorted_items, 2)):
                processes.append(multiprocessing.Process(target=self.__merge_wrapper,
                                                         args=(two_chunks[0],
                                                               two_chunks[1] if len(two_chunks) > 1 else list(),
                                                               merged_chunks, i)))

            handle_processes(processes)
            list_of_sorted_items = merged_chunks.values()
        return self.__merge(list_of_sorted_items[0], list_of_sorted_items[1])


@timeit
def built_in_sort(items):
    return sorted(items)


def generate_random_numbers(num_of_iterations, delta):
    import random
    for i in range(num_of_iterations):
        num_of_elements = (i + 1) * delta
        items = [random.randint(0, num_of_elements) for _ in range(0, num_of_elements)]
        yield items


def execute_by_random_generator():
    m = MergeSort()
    for items in generate_random_numbers(8, 300000):
        print(len(items))
        m.merge_sort_single_processed(items)
        m.merge_sort_multi_processed(items)
        built_in_sort(items)


def execute_from_file(file_path, num_of_processes):
    m = MergeSort()
    items = read_file(file_path)
    return m.merge_sort_multi_processed(items, num_of_processes)


def main(file_path):
    # execute_by_random_generator()
    execute_from_file(file_path, multiprocessing.cpu_count())

if __name__ == '__main__':
    main("./small_file.txt")
