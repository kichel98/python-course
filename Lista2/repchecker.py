import sys
import os
import hashlib
from collections import defaultdict


def get_all_pathfiles(start):
    paths = []
    for root, subdirs, files in os.walk(start):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths


def get_file_hash(file_path):
    buf_size = 32768  # Read file in 32kb chunks
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def prepare_file_stats(file_paths):
    stats = {}
    for path in file_paths:
        size = os.path.getsize(path)
        hash_value = get_file_hash(path)
        stats[path] = (size, hash_value)
    return stats


def group_duplicated_files(file_stats):
    grouped_dict = defaultdict(list)
    for path, stat in file_stats.items():
        grouped_dict[stat].append(path)

    return grouped_dict


def print_grouped_paths(grouped_dict):
    print("-----------------")
    for dup_paths in grouped_dict.values():
        for path in dup_paths:
            print(path)
        print("-----------------")


def main():
    file_paths = get_all_pathfiles(sys.argv[1])
    file_stats = prepare_file_stats(file_paths)
    grouped_dict = group_duplicated_files(file_stats)
    print_grouped_paths(grouped_dict)


main()
