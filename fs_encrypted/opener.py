from fs_encrypted.encrypted_fs import EncryptedFS
from fs.base import FS
from fs.opener.parse import ParseResult
from typing import Text

from fs.opener import Opener
from fs.opener.errors import OpenerError
from fs.opener.registry import registry

class EncryptedOpener(Opener) : 
    protocols = ["enc"]

    def open_fs(self, fs_url: Text, parse_result: ParseResult, writeable: bool, create: bool, cwd: Text) -> FS:
        path = parse_result.path
        resource = parse_result.resource
        
        key = parse_result.params.get("key")
        file_system = resource.split("/")[0]
        
        return EncryptedFS(resource, key)
    
registry.install(EncryptedOpener)