import tarfile
import os
from contextlib import contextmanager
import pwd
import grp
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

def chown(file, newuser, newgroup):
    with open(file, 'w') as file:
        user_name = newuser
        uid = pwd.getpwnam(user_name).pw_uid
        gid = grp.getgrnam(newgroup).gr_gid
        # Изменение владельца файла
        os.chown(file, uid, gid)
