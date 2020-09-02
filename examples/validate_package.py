#!/usr/bin/env python

import sys

from cdrouter import CDRouter

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <package-id>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
package_id = sys.argv[3]

c = CDRouter(base, token=token)

pkg = c.packages.get(package_id)
cfg = c.configs.get(pkg.config_id)

check = c.configs.check_config(cfg.contents)

print('Config contains {} error(s):'.format(len(check.errors)))
for e in check.errors:
    print('    {}: {}'.format(e.lines, e.error))
print('')

if len(check.errors) == 0:
    analysis = c.packages.analyze(pkg.id)

    print('{} of {} tests will be skipped:'.format(analysis.skipped_count, analysis.total_count))
    print('')
    for t in analysis.skipped_tests:
        print('    {} - {} >> {}'.format(t.name, t.skip_reason, t.skip_name))
