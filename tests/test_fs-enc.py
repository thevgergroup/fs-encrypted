'''
Main module for the EncryptedFS file system.
'''
from os import rmdir
import unittest
from fs_encrypted.encrypted_fs import EncryptedFS, encrypt, decrypt
from cryptography.fernet import Fernet
import inspect
import os

key = Fernet.generate_key()
base_dir = "./test_files"

class EncryptedFSTestCase(unittest.TestCase):
    def setUp(self):
        self.fs = EncryptedFS(base_dir, key)
        self.fs.makedirs("./test_dir")
        self.fs.writebytes("/test_file.txt", b"Hello, World!")
        
    def tearDown(self):
        
        self.fs.remove("/test_file.txt")
        self.fs.removedir("/test_dir")
        
    def test_getinfo(self):
        info = self.fs.getinfo("/test_file.txt", namespaces=["details"])
        self.assertEqual(info.name, "test_file.txt")
        self.assertEqual(info.is_dir, False)
        self.assertEqual(info.size, len(encrypt(b"Hello, World!", key)))
        
    def test_listdir(self):
        files = self.fs.listdir("/")
        self.assertSetEqual(set(files), set(["test_dir", "test_file.txt"]))

    def test_makedir(self):
        self.fs.makedir("/new_dir", recreate=True)
        self.assertTrue(self.fs.isdir("/new_dir"))
        self.fs.removedir("/new_dir")
        

    def test_openbin(self):
        with self.fs.openbin("/test_file.txt") as file:
            contents = file.read()
        self.assertEqual(contents, b"Hello, World!")

    def test_remove(self):
        self.fs.writebytes("/test_remove_file.txt", b"Hello, World!")
        self.fs.remove("/test_remove_file.txt")
        self.assertFalse(self.fs.exists("/test_remove_file.txt"))

    def test_removedir(self):
        self.fs.makedir("/test_remove_dir", recreate=True)
        self.fs.removedir("/test_remove_dir")
        self.assertFalse(self.fs.exists("/test_remove_dir"))

    def test_appendbytes(self):
        func_name = inspect.currentframe().f_code.co_name
        file_path = f"/{func_name}_file.txt"
        
        self.fs.writebytes(file_path, b"Hello, World!")
        self.fs.appendbytes(file_path, b", ChatDev")
        
        with self.fs.openbin(file_path) as file:
            contents = file.read()
        self.assertEqual(contents, b"Hello, World!, ChatDev")
        self.fs.remove(file_path)
        

    def test_appendtext(self):
        func_name = inspect.currentframe().f_code.co_name
        file_path = f"/{func_name}_file.txt"
        self.fs.writetext(file_path, "Hello, World!")
        self.fs.appendtext(file_path, ", ChatDev")
        with self.fs.openbin(file_path) as file:
            contents = file.read()
        self.assertEqual(contents, b"Hello, World!, ChatDev")
        self.fs.remove(file_path)
        


    def test_close(self):
        fs2 = EncryptedFS("./test_files2", key)
        fs2.close()
        self.assertTrue(fs2.isclosed())
        rmdir("./test_files2")
        
   
    def test_copy(self):
        self.fs.copy("/test_file.txt", "/test_dir/test_file_copy.txt")
        self.assertTrue(self.fs.exists("/test_dir/test_file_copy.txt"))
        self.fs.remove("/test_dir/test_file_copy.txt")


    def test_copydir(self):
        self.fs.copydir("/test_dir", "/new_dir", create=True)
        self.assertTrue(self.fs.exists("/new_dir"))
        self.fs.removedir("/new_dir")

    def test_exists(self):
        self.assertTrue(self.fs.exists("/test_file.txt"))
        self.assertFalse(self.fs.exists("/nonexistent_file.txt"))
        
    def test_open(self):
        with self.fs.open("/test_file.txt") as file:
            contents = file.read()
        self.assertEqual(contents, b"Hello, World!")

    def test_opendir(self):
        func_name = inspect.currentframe().f_code.co_name
        file_path = f"/test_dir/{func_name}_file.txt"
        
        self.fs.makedir("/test_dir", recreate=True)
        self.fs.writetext(file_path, "Hello, World!")
        
        with self.fs.opendir("/test_dir") as dir:
            files = dir.listdir('./')
        self.assertEqual(files, [file_path.split('/')[-1]])
        self.fs.remove(file_path)
        

    def test_readbytes(self):
        contents = self.fs.readbytes("/test_file.txt")
        self.assertEqual(contents, b"Hello, World!")


    @unittest.skip("Not implemented")
    def test_writefile(self):
        with self.fs.openbin("/test_file.txt") as file:
            self.fs.writefile("/new_file.txt", file)
        
        self.assertTrue(self.fs.exists("/new_file.txt"))

    def test_readtext(self):
        
        contents = self.fs.readtext("/test_file.txt")
        self.assertEqual(contents, "Hello, World!")

    def test_writetext(self):
        func_name = inspect.currentframe().f_code.co_name
        file_path = f"/{func_name}_file.txt"
        
        self.fs.writetext(file_path, "Hello, ChatDev!")
        self.assertTrue(self.fs.exists(file_path))
        contents = self.fs.readtext(file_path)
        self.assertEqual(contents, "Hello, ChatDev!")
        self.fs.remove(file_path)
        


    def test_isfile(self):
        self.assertTrue(self.fs.isfile("/test_file.txt"))
        self.assertFalse(self.fs.isfile("/test_dir"))

    def test_isdir(self):
        self.assertTrue(self.fs.isdir("/test_dir"))
        self.assertFalse(self.fs.isdir("/test_file.txt"))


    def test_desc(self):
        desc = self.fs.desc("/test_file.txt")
        cwd = os.getcwd()
        self.assertEqual(desc, os.path.join(cwd, base_dir[2:], "test_file.txt"))

    @classmethod
    def tearDownClass(cls):
        rmdir(base_dir)

if __name__ == "__main__":
    unittest.main()