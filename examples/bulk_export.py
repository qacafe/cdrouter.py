#!/usr/bin/env python

import sys
import shutil

from cdrouter import CDRouter
from cdrouter.configs import Config

if len(sys.argv) < 3:
    print('usage: <base_url> <token> [<config-ids>] [<device-ids>] [<package-ids>] [<result-ids>]')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]

config_ids = None
device_ids = None
package_ids = None
result_ids = None

if len(sys.argv) > 3 and len(sys.argv[3]) > 0:
    config_ids = [int(x.strip()) for x in sys.argv[3].split(',')]

if len(sys.argv) > 4 and len(sys.argv[4]) > 0:
    device_ids = [int(x.strip()) for x in sys.argv[4].split(',')]

if len(sys.argv) > 5 and len(sys.argv[5]) > 0:
    package_ids = [int(x.strip()) for x in sys.argv[5].split(',')]

if len(sys.argv) > 6 and len(sys.argv[6]) > 0:
    result_ids = [int(x.strip()) for x in sys.argv[6].split(',')]

c = CDRouter(base, token=token)

b, filename = c.exports.bulk_export(
    config_ids=config_ids,
    device_ids=device_ids,
    package_ids=package_ids,
    result_ids=result_ids
)

with open(filename, 'wb') as fd:
    shutil.copyfileobj (b, fd)

print(filename)
