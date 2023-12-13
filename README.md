## FS-Encrypted 

- [FS-Encrypted](#fs-encrypted)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usages](#usages)
  - [Development](#development)


### Introduction

The EncryptedFS is a file system implementation that provides encryption and decryption functionalities for files. It is built using PyFilesystem and AES encryption. 
This allows minimal modification for existing applications to use
Example: 

```python

from fs_encrypted.encrypted_fs import EncryptedFS
import base64

#Generate and Store your keys securely !!!
key = base64.urlsafe_b64encode(b"Hello I'm a 32bit encoded string") 

# Create a directory called secure_data 
file_system = EncryptedFS("./secure_data", key)

# create a file called my_secrets.txt and encrypt as it's written to
with file_system.open("my_secrets.txt", "w") as file : 
   file.write(b"Top Secret Data!!")

# read and decrypt my_secrets
with file_system.open("my_secrets.txt", "r") as file : 
   file.read()

```

### Installation

Use pip or poetry to install
```
pip install fs-encrypted
```
or 
```
poetry add fs-encrypted
```

### Usages 
Applications that may require sensitive data storage should use an encrypted file system.
By providing a layer of abstraction on top of the encryption our hope is to make it easier to store this data.

* PII / PHI 
  * Print Billing systems 
  * Insurance services / Identity cards 
* Data Transfer 
* Secure distributed configuration


Fernet is used as the encryption method (v0.1), this may become a configurable option in future revisions


### Development

Clone the fs-encrypted repository https://github.com/thevgergroup/fs-encrypted

Development is done using poetry

Tests are run as 
```
poetry run python -m unittest tests/*.py
```


