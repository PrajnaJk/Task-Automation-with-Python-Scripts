import os
import shutil


def organize_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = filename.split('.')[-1]
            target_dir = os.path.join(directory, file_ext)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.move(file_path, os.path.join(target_dir, filename))
