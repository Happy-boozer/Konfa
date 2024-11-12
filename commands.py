from contextlib import contextmanager
import os
import tarfile
import shutil
import pwd
import grp
import sys
import argparse



class ShellEmulator:
    def __init__(self, tar_path, hostname="localhost"):
        self.hostname = hostname
        self.fs_path = "/tmp/emulated_fs"
        self.mount_fs(tar_path)

    def ls(self, path="."):
        # Получаем список файлов в указанной директории
        full_path = os.path.join(self.fs_path, path)
        try:
            files = os.listdir(full_path)
            for f in files:
                print(f)
        except FileNotFoundError:
            print(f"ls: cannot access '{path}': No such file or directory")

    def cd(self, path):
        # Переход в другую директорию
        full_path = os.path.join(self.fs_path, path)
        if os.path.isdir(full_path):
            os.chdir(full_path)
        else:
            print(f"cd: {path}: No such directory")

    def chown(self, user, group, path):
        # Изменение владельца и группы файла
        full_path = os.path.join(self.fs_path, path)
        try:
            uid = pwd.getpwnam(user).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(full_path, uid, gid)
        except KeyError:
            print(f"chown: invalid user or group: {user}:{group}")
        except FileNotFoundError:
            print(f"chown: {path}: No such file or directory")

    def echo(self, text):
        # Вывод текста на экран
        print(text)