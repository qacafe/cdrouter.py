#!/usr/bin/python

import sys
import time

from cdrouter import CDRouter
from cdrouter.jobs import Job

if len(sys.argv) < 3:
    print 'usage: <base_url> <token> [<tag>]'
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
tag_name = 'nightly'

if len(sys.argv) > 3:
    tag_name = sys.argv[3]

# create service
c = CDRouter(base, token=token)

packages = c.packages.list(filter=['tags@>{'+tag_name+'}'])
jobs = [Job(package_id=p.id) for p in packages]

for j in c.jobs.bulk_launch(jobs=jobs):
    while j.result_id is None:
        time.sleep(1)
        j = c.jobs.get(j.id)
    print j.result_id
