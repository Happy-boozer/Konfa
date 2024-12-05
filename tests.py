import unittest

from unittest.mock import patch, MagicMock
import os
import tarfile
from io import StringIO

class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.archive = tarfile.open(tar_path, "r")

    def list_files(self, path="."):
        # Получаем список файлов в виртуальной директории
        path = path.lstrip('/')  # Убираем ведущий слэш, если есть
        file_names = []
        for member in self.archive.getmembers():
            if member.name.startswith(path):
                file_names.append(member.name[len(path):].lstrip('/'))  # Отрезаем путь
        return file_names

    def is_dir(self, path):
        # Проверяем, существует ли директория в архиве
        path = path.lstrip('/')
        for member in self.archive.getmembers():
            if member.name == path and member.isdir():
                return True
        return False

class ShellEmulator:
    def __init__(self, tar_path, hostname="localhost"):
        self.hostname = hostname
        self.fs = VirtualFileSystem(tar_path)
        self.current_directory = "/"

    def ls(self, path=""):
        # Получаем список файлов в указанной директории
        if path == "":
            path = self.current_directory

        files = self.fs.list_files(path)
        if files:
            for f in files:
                print(f)
        else:
            print(f"ls: cannot access '{path}': No such file or directory")

    def cd(self, path):
        # Переход в другую директорию
        full_path = os.path.join(self.current_directory, path).lstrip('/')
        if self.fs.is_dir(full_path):
            self.current_directory = full_path
        else:
            print(f"cd: {path}: No such directory")

    def chown(self, user, group, path):
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
        print(f"chown: {user}:{group} {path}")

    def echo(self, text):
        # Вывод текста на экран
        print(text)

    def run(self):
        while True:
            command = input(f"{self.hostname}$ ").strip()
            if command.startswith("ls"):
                parts = command.split()
                path = parts[1] if len(parts) > 1 else self.current_directory
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



class TestShellEmulator(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    @patch("tarfile.open")
    def test_ls(self, mock_tarfile, mock_stdout):
        # Mock the tarfile and its members
        mock_member_1 = MagicMock()
        mock_member_1.name = 'file1.txt'
        mock_member_1.isdir.return_value = False
        mock_member_2 = MagicMock()
        mock_member_2.name = 'dir/file2.txt'
        mock_member_2.isdir.return_value = False

        mock_tar = MagicMock()
        mock_tar.getmembers.return_value = [mock_member_1, mock_member_2]
        mock_tarfile.return_value = mock_tar

        emulator = ShellEmulator("nry.tar")

        # Simulate 'ls' command
        emulator.ls()

        output = mock_stdout.getvalue().strip()
        self.assertIn('file1.txt', output)
        self.assertIn('dir/file2.txt', output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("tarfile.open")
    def test_cd(self, mock_tarfile, mock_stdout):
        # Mock the tarfile and its members
        mock_member_1 = MagicMock()
        mock_member_1.name = 'dir'
        mock_member_1.isdir.return_value = True
        mock_member_2 = MagicMock()
        mock_member_2.name = 'file1.txt'
        mock_member_2.isdir.return_value = False

        mock_tar = MagicMock()
        mock_tar.getmembers.return_value = [mock_member_1, mock_member_2]
        mock_tarfile.return_value = mock_tar

        emulator = ShellEmulator("nry.tar")

        # Test valid directory change
        emulator.cd("dir")
        self.assertEqual(emulator.current_directory, "dir")

        # Test invalid directory change
        emulator.cd("nonexistent")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "cd: nonexistent: No such directory")

    @patch("sys.stdout", new_callable=StringIO)
    def test_chown(self, mock_stdout):
        emulator = ShellEmulator("nry.tar")

        # Test chown command
        emulator.chown("user", "group", "file1.txt")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "chown: user:group file1.txt")

    @patch("sys.stdout", new_callable=StringIO)
    def test_echo(self, mock_stdout):
        emulator = ShellEmulator("nry.tar")

        # Test echo command
        emulator.echo("Hello, world!")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Hello, world!")


if __name__ == "__main__":
    unittest.main()
