import sys

from merge_sort import execute_from_file


def valid_num_of_arguments():
    if len(sys.argv) != 3:
        print("Please enter a valid number of arguments")
        sys.exit(1)


def convert_num_of_processes_to_number(num_of_processes):
    if not num_of_processes.isdigit():
        print("Please enter a valid formatted number of processes")
        sys.exit(1)
    return int(num_of_processes)


def at_least_two_processes(num_of_processes):
    if num_of_processes < 2:
        print("Please enter number of processes higher than 1")
        sys.exit(1)


def valid_num_of_processes(num_of_processes):
    num_of_processes = convert_num_of_processes_to_number(num_of_processes)
    at_least_two_processes(num_of_processes)
    return num_of_processes


def validate_arguments():
    valid_num_of_arguments()
    num_of_processes, file_path = sys.argv[1:3]
    num_of_processes = valid_num_of_processes(num_of_processes)
    return num_of_processes, file_path


def main():
    num_of_processes, file_path = validate_arguments()
    sorted_items = execute_from_file(file_path, int(num_of_processes))
    print("\n".join(map(str, sorted_items)))

if __name__ == '__main__':
    main()
