#!/usr/bin/env python

import sys

from cdrouter import CDRouter
from cdrouter.jobs import Job

if len(sys.argv) < 6:
    print('usage: <base_url> <token> <device-name> <software-version> <software>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
device_name = sys.argv[3]
software_version = sys.argv[4]
software = sys.argv[5]

c = CDRouter(base, token=token)

d = c.devices.list(filter=['name='+device_name], limit='1').data[0]

d.software_version = software_version
d = c.devices.edit(d)

a = c.attachments.create(d.id, software)
a.description = 'Firmware for {}'.format(software_version)
a = c.attachments.edit(a)

packages = c.packages.list(filter=['device_id='+d.id], limit='none').data
jobs = [Job(package_id=p.id, tags=[software_version]) for p in packages]

c.jobs.bulk_launch(jobs)
