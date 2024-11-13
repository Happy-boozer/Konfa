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

    def run(self):
        while True:
            command = input(f"{self.hostname}$ ").strip()
            if command.startswith("ls"):
                parts = command.split()
                path = parts[1] if len(parts) > 1 else "."
                self.ls(path)
            elif command.startswith("cd"):
                parts = command.split()
                if len(parts) > 1:
                    self.cd(parts[1])
                else:
                    print("cd: missing operand")
            elif command.startswith("chown"):
                parts = command.split()
                if len(parts) > 2:
                    user, group = parts[1].split(":")
                    self.chown(user, group, parts[2])
                else:
                    print("chown: missing operand")
            elif command.startswith("echo"):
                parts = command.split(maxsplit=1)
                if len(parts) > 1:
                    self.echo(parts[1])
                else:
                    print("echo: missing operand")
            elif command == "exit":
                break
            else:
                print(f"{command}: command not found")

def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("hostname", help="Hostname for the shell prompt")
    parser.add_argument("tar_path", help="Path to the tar archive containing the virtual filesystem")
    args = parser.parse_args()

    emulator = ShellEmulator(args.tar_path, args.hostname)
    emulator.run()

if __name__ == "__main__":
    main()