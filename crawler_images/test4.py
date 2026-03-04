import os
import random

# os.rename(old_name, new_name)

dirs = [
    "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page0000--page0100\\0001",
    "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page0000--page0100\\0002",
    "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page0000--page0100\\0003",
]


for sub_dir in dirs:
    os.chdir(sub_dir)

    sub_dirs = os.listdir(sub_dir)

    for dir_name in sub_dirs:
        new_dir_name = ''
        index = dir_name.find(" - ")
        if index > 0:
            new_dir_name = dir_name[:index] + " - " + str(random.randint(100000, 999999))
        else:
            index = dir_name.find("-")
            if index > 0:
                new_dir_name = dir_name[:index] + " - " + str(random.randint(100000, 999999))

        if new_dir_name:
            os.rename(dir_name, new_dir_name)
