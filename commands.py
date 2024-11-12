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
