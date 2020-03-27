#!/usr/bin/env python
# https://stackoverflow.com/questions/545387/linux-compute-a-single-hash-for-a-given-folder-contents
import base64
import hashlib
import json
import os
import sys
from glob import iglob
from subprocess import check_output

files = [os.path.realpath(x)
         for x in iglob(f'{sys.argv[1]}/**', recursive=True)
         if os.path.isfile(x)]

hashes = check_output(
    ['git', 'hash-object', '--stdin-paths'],
    input='\n'.join(files).encode(),
)

sha256 = hashlib.sha256(hashes).digest()
result = {'hash': base64.b64encode(sha256).decode()}

print(json.dumps(result))
