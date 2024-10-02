import tarfile
import os
from contextlib import contextmanager
def echo(*args):
    print(*args)

def ls():
    tar = tarfile.open("nry.tar")
    namelist = tar.getnames()
    for file in namelist:
        print(file)

def exit():
    return True

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)