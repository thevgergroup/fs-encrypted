from fs_encrypted.encrypted_fs import EncryptedFS
from fs_encrypted.pathlike import FSPathLike
import base64

key = base64.urlsafe_b64encode(b'123456789012345678901234567890121')

path = FSPathLike(f"enc://files/test_files?key={key}")

with open(path, "w") as file:
    file.write("Hello, World!")