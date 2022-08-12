import os
from sys import argv


def union_files_with_deletion(files_dir, del_pattern, union_dir="generated_file_unions/"):
    deleted_count = 0
    if not os.path.isdir(union_dir):
        os.mkdir(union_dir)
        print(f"Directory {union_dir} created.")

    union_file_path = os.path.join(union_dir, "union.txt")

    with open(union_file_path, "w", encoding="utf-8") as fw:
        if not os.path.isdir(files_dir) or len(os.listdir(files_dir)) == 0:
            raise FileNotFoundError("Run files_generation.py to automatically create files directory and fill it.")
        else:
            file_names_list = os.listdir(files_dir)
            for file_name in file_names_list:
                file_path = os.path.join(files_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as fr:
                    for row in fr:
                        if (del_pattern is not None) and (del_pattern in row):
                            deleted_count += 1
                            continue

                        fw.write(row)

    return deleted_count


try:
    arg_files_dir = argv[1]
    arg_del_pattern = argv[2]
except IndexError:
    print("This script requires additional arguments. Default arguments will be used.\n")
    arg_files_dir = "generated_files/"
    arg_del_pattern = None

print(f"Files directory: {arg_files_dir}\nDeletion pattern: {arg_del_pattern}")

deleted_rows_count = union_files_with_deletion(arg_files_dir, arg_del_pattern)
print(f"Union completed. Deleted rows count: {deleted_rows_count}")
