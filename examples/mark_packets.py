#!/usr/bin/env python

import sys

from cdrouter import CDRouter
from cdrouter.highlights import Highlight

if len(sys.argv) < 3:
    print('usage: <base_url> <token>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]

c = CDRouter(base, token=token)

for r in c.results.iter_list(sort=['-id']):
    for tr in c.tests.iter_list(r.id):
        try:
            logs = c.tests.list_log(tr.id, tr.seq, filter=['proto=DHCP', 'info~*offer'], limit='100000')
        except:
            continue

        if len(logs.lines) == 0:
            continue

        r.starred = True
        r = c.results.edit(r)

        print('{}: starred'.format(r.id))

        tr.flagged = True
        tr = c.tests.edit(tr.id, tr)

        print('{}: {}: flagged'.format(r.id, tr.name))

        for log in logs.lines:
            c.highlights.create(tr.id, tr.seq,
                                Highlight(line=str(log.line), color='red'))

            print('{}: {}: line {}: highlighted red'.format(r.id, tr.name, log.line))

