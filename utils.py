import os

def make_dir_w_exception(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        print("Output folder for this run already exists.")