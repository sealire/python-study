import os
import re

root_dir = "F:\\GIT\\python-study\\crawler_images\\images"


def get_sub_dirs(dir):
    return os.listdir(dir)


def change_dir_name(dir):
    sub_dir_names = get_sub_dirs(dir)
    for sub_dir_name in sub_dir_names:
        current_dir = os.path.join(dir, sub_dir_name)
        if not os.path.isdir(current_dir):
            continue

        new_sub_dir_name = re.sub(r"[～~@!?/'.]", '', sub_dir_name)
        new_sub_dir_name = new_sub_dir_name.strip()
        if new_sub_dir_name != sub_dir_name:
            os.chdir(dir)
            print(f"{new_sub_dir_name:<50}, {sub_dir_name:<50}")
            os.rename(sub_dir_name, new_sub_dir_name)

        new_dir = os.path.join(dir, new_sub_dir_name)
        change_dir_name(new_dir)


change_dir_name(root_dir)
