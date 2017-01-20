#!/usr/bin/env python

import sys

from cdrouter import CDRouter

if len(sys.argv) < 3:
    print('usage: <base_url> <token>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]

c = CDRouter(base, token=token)

for r in c.results.list(filter=['fail>0'], sort=['-id'], limit=25):
    for tr in c.tests.list(r.id, filter=['result=fail'], limit='none'):
        logs = c.tests.get_log(tr.id, tr.seq, filter=['prefix=FAIL'], limit='100000')
        msg = ' '.join([log.message for log in logs.lines])
        print('Result {}: Test {}: Name {}: {}'.format(r.id, tr.seq, tr.name, msg))
