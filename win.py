from contextlib import contextmanager
import os
import tarfile
import shutil
import argparse


class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.archive = tarfile.open(tar_path, "r")
        self.file_owners = {}

        for member in self.archive.getmembers():
            if member.isfile():
                # Присваиваем владельца
                self.file_owners[member.name] = "user"

    def list_files(self, path="."):
        # Получаем список файлов в виртуальной директории
        path = path.lstrip('/')  # Убираем ведущий слэш, если есть
        file_info = []
        for member in self.archive.getmembers():
            #print(member)
            #print(member.name[len(path):].lstrip('/'))
            owner= "user"
            file_info.append((member.name[len(path):].lstrip('/'), owner))
            """if member.name.startswith(path) and member.name.count('/') == path.count('/'):

                owner = self.file_owners.get(member.name, "unknown")
                file_info.append((member.name[len(path):].lstrip('/'), owner))
        #print(file_info)"""
        return file_info

    def is_dir(self, path):
        # Проверяем, существует ли директория в архиве
        path = path.lstrip('/')

        for member in self.archive.getmembers():
            if member.name == path and member.isdir():
                print(member.name)
                return True

        return False

    def change_owner(self, path, new_owner):
        # Функция для изменения владельца файла
        if path in self.file_owners:
            self.file_owners[path] = new_owner


class ShellEmulator:
    def __init__(self, tar_path, hostname="localhost"):
        self.hostname = hostname
        self.fs = VirtualFileSystem(tar_path)
        self.current_directory = "/"

    """    def ls(self, path=""):
        # Получаем список файлов в указанной директории"""

    def ls(self, path=""):
        if path:
            full_path = os.path.join(self.current_directory, path)
            files = self.fs.list_files(full_path)
        else:
            files = self.fs.list_files(self.current_directory)

        if files:
            for f, owner in files:
                print(f"{f} (owner: {owner})")
        else:
            print("Directory is empty.")
     # Получаем список файлов в текущей директории
        """    files = self.fs.list_files(self.current_directory)
        if files:
            for f in files:
                    print(f)
        else:
                print("Directory is empty.")"""

        """# Получаем список файлов в текущей директории с владельцами
        files = self.fs.list_files(self.current_directory)
        #print(files)
        if files:
            for f, owner in files:
                print(f"{f} (owner: {owner})")
        else:
            print("Directory is empty.")
        """
    def cd(self, path):
        # Переход в другую директорию
        full_path = os.path.join(self.current_directory, path).lstrip('/')
        #print(full_path)
        #print(full_path.find("\\"))
        pos = full_path.find("\\")
        f = full_path.split("\\")
        fp = ""
        #f.join("/")

        for i in range(len(f) - 1):
            fp += f[i] + "/"
        fp += f[-1]
        print(fp)
        if path == "..":
            # Переход на уровень выше
            if self.current_directory != "/":
                self.current_directory = '/'.join(self.current_directory.split('/')[:-1]) or '/'
        else:
            if self.fs.is_dir(fp):
                self.current_directory = full_path
            else:
                print(f"cd: {path}: No such directory")


    """def cd(self, path):
        # Переход в указанную директорию, поддержка перехода на уровень выше
        if path == "..":
            # Переход на уровень выше
            if self.current_directory != "/":
                self.current_directory = '/'.join(self.current_directory.split('/')[:-1]) or '/'
        else:
            # Переход в указанную директорию
            if self.fs.is_dir(os.path.join(self.current_directory, path)):
                self.current_directory = os.path.join(self.current_directory, path)
            else:
                print(f"cd: no such file or directory: '{path}'")
    """
    def pwd(self):
        # Печатает текущую рабочую директорию
        print(self.current_directory)

    def chown(self, file_name, new_owner):
        # Изменяет владельца файла
        full_path = os.path.join(self.current_directory, file_name)
        if self.fs.is_dir(full_path) or any(f for f in self.fs.list_files(self.current_directory) if f == file_name):
            self.fs.change_owner(full_path, new_owner)
            print(f"Owner of '{file_name}' changed to {new_owner}.")
        else:
            print(f"chown: no such file or directory: '{file_name}'")
        """# Изменение владельца и группы файла
        full_path = os.path.join(self.fs_path, path)
        shutil.chown(full_path, user=None, group=None)

        try:
            uid = pwd.getpwnam(user).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(full_path, uid, gid)
        except KeyError:
            print(fchown: invalid user or group: {user}:{group}")
        except FileNotFoundError:
            print(f"chown: {path}: No such file or directory")"""
        #print(f"chown: {user}:{group} {path}")

    def echo(self, text):
        # Вывод текста на экран
        print(text)

    def run(self):
        while True:
            command = input(f"{self.hostname}$ ").strip()
            if command.startswith("ls"):
                parts = command.split()
                path = parts[1] if len(parts) > 1 else self.current_directory
                self.ls()
            elif command.startswith("cd"):
                parts = command.split()
                if len(parts) > 1:
                    self.cd(parts[1])
                else:
                    print("cd: missing operand")
            elif command.startswith("chown"):
                parts = command.split()
                #print(parts)
                if len(parts) > 2:
                    file_name = parts[1]
                    new_owner = parts[2]
                    self.chown(file_name, new_owner)
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
