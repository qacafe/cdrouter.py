#!/usr/bin/env python

import sys
import time

from cdrouter import CDRouter
from cdrouter.configs import Testvar
from cdrouter.jobs import Job

if len(sys.argv) < 4:
    print('usage: <base_url> <token> "<package name>"')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
package_name = sys.argv[3]

# create service
c = CDRouter(base, token=token)

p = c.packages.get_by_name(package_name)
if not p:
    sys.exit("Package {0} not found.".format(package_name))


print('Running package {0}'.format(package_name))
print('')

j = c.jobs.launch(Job(package_id=p.id))

# wait for job to be assigned a result ID
while j.result_id is None:
    time.sleep(1)
    j = c.jobs.get(j.id)

print('        Result-ID: {0}'.format(j.result_id))
print('')

print('        Waiting for job to complete...')
u = c.results.updates(j.result_id, None)
while u:
    r = c.results.get(j.result_id)
    if r.status in ['completed', 'stopped', 'error']:
        break
    print('        Progress: {0}%'.format(u.progress.progress))
    u = c.results.updates(j.result_id, u.id)

print('        Job status: {0}'.format(r.status))
print('')

filename = 'results_{0}.xml'.format(j.result_id)
print('Writing results to file "{0}" in Jenkins XML format'.format(filename))
with open(filename, 'w') as f:
    f.write('<testsuite name="CDRouter" package="{0}" failures="{1}" tests="{2}">\n'.format(package_name, r.fail, r.tests))
    for t in c.tests.iter_list(j.result_id):
        f.write('    <testcase name="{0}">\n'.format(t.name))
        if t.result in ['fail', 'fatal']:
            f.write('        <failure message="test failures">')
            f.write('View the full CDRouter test log {0}'.format(base+'/results/'+str(j.result_id)+'/tests/'+str(t.seq)))
            f.write('</failure>\n')
        elif t.result in ['pending', 'skipped']:
            f.write('        <skipped/>\n')
            f.write('    </testcase>\n')
            f.write('</testsuite>\n')
            f.close()

print('done')

