#!/usr/bin/env python

import sys

from cdrouter import CDRouter
from cdrouter.configs import Config

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <result-ids>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]

result_ids = None
if len(sys.argv) > 3 and len(sys.argv[3]) > 0:
    result_ids = [int(x.strip()) for x in sys.argv[3].split(',')]

c = CDRouter(base, token=token)

diff = c.results.diff_stats(result_ids)

for test in diff.tests:
    print('name: {}'.format(test.name))
    for summary in test.summaries:
        print('  id: {}'.format(summary.id))
        print('  seq: {}'.format(summary.seq))
        print('  result: {}'.format(summary.result))
        print('  duration: {}'.format(summary.duration))
        print('  flagged: {}'.format(summary.flagged))
        print('  name: {}'.format(summary.name))
        print('  description: {}'.format(summary.description))
