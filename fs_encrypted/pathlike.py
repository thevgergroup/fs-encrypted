'''
A PathLike subclass that allows pythons open method to work with pyfilesystem2.
'''
from os import PathLike
#from pathlib import Path
try:
    from fs import open_fs
except ModuleNotFoundError:
    print("ModuleNotFoundError: No module named 'fs'")
    print("Please make sure you have installed the 'fs' module.")
    exit(1)
class FSOpen:
    def __init__(self, fs_url):
        self.fs_url = fs_url
    def __fspath__(self):
        return self.fs_url
    def __enter__(self):
        self.fs = open_fs(self.fs_url)
        self.file = self.fs.open(str(self))
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.fs.close()
class FSPathLike(PathLike):
    def __init__(self, fs_url):
        self.fs_url = fs_url
    def __fspath__(self):
        print("Opening 1", self.fs_url)
        return self.fs_url
    
    def open(self, mode='r', **kwargs):
        print("Opening", self.fs_url)
        return FSOpen(self.fs_url)