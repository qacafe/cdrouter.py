#!/usr/bin/env python

import os
import shutil
import sys

from cdrouter import CDRouter

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <file>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
filepath = sys.argv[3]
filename = os.path.basename(filepath)

c = CDRouter(base, token=token)

d = c.custom_files.mkdir('example-dir')
print(d.name, d.is_dir)

with open(filepath, 'rb') as fd:
    f = c.custom_files.upload('example-dir', fd, filename=filename)
print(f.name, f.size)

entries = c.custom_files.list('example-dir')
for entry in entries:
    print(entry.name, entry.size, entry.is_dir)

info = c.custom_files.get('example-dir/' + filename)
print(info.name, info.size, info.modified)

b, dl_filename = c.custom_files.download('example-dir/' + filename)
with open(dl_filename, 'wb') as fd:
    shutil.copyfileobj(b, fd)
print(dl_filename)

f = c.custom_files.rename('example-dir/' + filename, 'renamed-' + filename)
print(f.name)

c.custom_files.delete('example-dir', recursive=True)
