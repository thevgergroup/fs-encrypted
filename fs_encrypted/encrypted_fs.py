'''
Module for the EncryptedFS file system implementation.
'''
from typing import IO, Any, AnyStr, BinaryIO, Optional, Text
from fs.osfs import OSFS
from functools import partial
from fs.wrapfs import WrapFS
from cryptography.fernet import Fernet


class EncryptedFS(WrapFS):
    def __init__(self, root_path, encryption_key):
        self.encryption_key = encryption_key
        #self.cipher_suite = Fernet(encryption_key)
        self.inner_fs = OSFS(root_path, create=True)
        super().__init__(self.inner_fs)

    def writebytes(self, path, data):
        encrypted_data = encrypt(data, self.encryption_key)
        super().writebytes(path, encrypted_data)
    
    def writetext(self, path: Text, contents: Text, encoding: Text = "utf-8", errors: Text | None = None, newline: Text = "") -> None:
        # TODO: handle errors and newline
        # Shorcut for writing text as all text is encoded to bytes anyway
        self.write(path, contents.encode(encoding))
        
    
    def readbytes(self, path):
        encrypted_data = super().readbytes(path)
        decrypted_data = decrypt(encrypted_data, self.encryption_key)
        return decrypted_data

    def appendbytes(self, path: Text, data: bytes) -> None:
        return super().appendbytes(path, encrypt(data, self.encryption_key))

    def appendtext(self, path: Text, text: Text, encoding: Text = "utf-8", errors: Text | None = None, newline: Text = "") -> None:
        data = encrypt(bytes(text, encoding), self.encryption_key)
        #print(data)
        return super().appendtext(path, data.decode(encoding), encoding, errors, newline)
    
    
    def readtext(self, path: Text, encoding: Text = "utf-8", errors: Text | None = None, newline: Text = "") -> Text:
        return decrypt(super().readtext(path, encoding, errors, newline).encode(encoding), self.encryption_key).decode(encoding)
    

    def read(self, size: Optional[int] = None, path :Optional[str] = None) -> bytes:
        return self.readbytes(path=path)
        
        

    def write(self, path: Text, data: bytes, chunk_size: int = 64 * 1024) -> int:
        # chunk data into chunk_size
        length = len(data)
        for i in range(0, length, chunk_size):
            super().writebytes(path, encrypt(data[i:i+chunk_size], self.encryption_key))
        return length
    
    def io_write(self, data: bytes, io, chunk_size: int = 64 * 1024) -> int:
        
        return io._write(encrypt(data, self.encryption_key).decode("utf-8"))
    
        
    # Provide new read / write methods for the binary io object
    def openbin(self, path: Text, mode: Text = "r", buffering: int = -1, **options: Any) -> BinaryIO:
        io =  super().openbin(path, mode, buffering, **options)
        io._read = io.read
        io.read = partial(self.read, path=path)
        io._write = io.write
        io.write = self.write
        io.readtext = partial(self.readtext, path=path)
        
        return io
    
    # Provide new read / write methods for the io object
    def open(self, path: Text, mode: Text = "r", buffering: int = -1, encoding: Text | None = None, errors: Text | None = None, newline: Text = "", line_buffering: bool = False, **options: Any) -> IO[AnyStr]:
        
        io = super().open(path, mode, buffering, encoding, errors, newline, line_buffering, **options)
        
        io._read = io.read
        io.read = partial(self.read, path=path)
        io._write = io.write
        io.write = partial(self.io_write, io=io)
        
        return io
    
    def desc(self, path: Text) -> Text:
        return self.inner_fs.desc(path)
        


    
def encrypt(data :bytes , encryption_key) -> bytes:
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.encrypt(data)



def decrypt(data : str, encryption_key) -> bytes:
    
    # As data can be appended to a file, the data may consist of multiple encrypted chunks
    # Each chunk is separated by a "==" 
    
    lines = data.split(b"==", )
    cipher_suite = Fernet(encryption_key)
    dec = b""
    for line in lines:
        line += b"=="
        if line == b"==":
            continue
        
        dec += cipher_suite.decrypt(line)
        
    return dec