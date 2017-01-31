#!/usr/bin/env python

import os
import sys

from cdrouter import CDRouter

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <archive>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
archive = sys.argv[3]

# create service
c = CDRouter(base, token=token)

with open(archive, 'r+') as fd:
    si = c.imports.stage_import_from_file(fd, filename=os.path.basename(archive))

impreq = c.imports.get_commit_request(si.id)

for name in impreq.configs:
    impreq.configs[name].should_import = True
for id in impreq.packages:
    impreq.packages[id].should_import = True
for id in impreq.devices:
    impreq.devices[id].should_import = True
for id in impreq.results:
    impreq.results[id].should_import = True

resp = c.imports.commit(si.id, impreq)

print(resp.configs)
print(resp.packages)
print(resp.devices)
print(resp.results)
