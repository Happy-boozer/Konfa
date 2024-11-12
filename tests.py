import unittest
import os
import tempfile
import shutil
import tarfile
from commands import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создаем временный каталог для тестов
        self.test_dir = tempfile.mkdtemp()
        self.create_test_tar()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_test_tar(self):
        # Создаем тестовый tar архив
        with tarfile.open(os.path.join(self.test_dir, "fs.tar"), "w") as tar:
            os.mkdir(os.path.join(self.test_dir, "test_dir"))
            tar.add(os.path.join(self.test_dir, "test_dir"), arcname="test_dir")

    def test_ls(self):
        # Проверим команду ls
        emulator = ShellEmulator(os.path.join(self.test_dir, "fs.tar"))
        # Здесь, например, можно переопределить метод ls для проверки вывода
        emulator.ls()  # Ожидаем, что в выводе будет "test_dir"
