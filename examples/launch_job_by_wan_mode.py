#!/usr/bin/python

import re
import sys
import time

from cdrouter import CDRouter
from cdrouter.configs import Testvar
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

# get array of all possible values for wanMode
choices = c.testsuites.get_testvar('wanMode').keywords

print '{0} possible WAN modes defined: {1}'.format(len(choices), choices)
print ''

# find all packages with given tag
packages = c.packages.list(filter=['tags@>{'+tag_name+'}'], limit='none')

print 'Found {0} packages with {1} tag'.format(len(packages), tag_name)
print ''

# loop over each package
for p in packages:
    # look for tags matching valid wanMode values
    wan_modes = [itm for itm in choices if itm in p.tags]

    # skip package if it has no wanMode tags or if it has no config
    if len(wan_modes) == 0 or p.config_id == '0':
        continue

    print 'Running package {0} with WAN modes: {1}'.format(p.name, wan_modes)
    print ''

    # save the original wanMode value from the package's config
    orig = c.configs.get_testvar(p.config_id, name='wanMode').value

    # loop over each wanMode value
    for v in wan_modes:
        # set wanMode in package's config to v
        print '   Setting wanMode to {0}'.format(v)
        c.configs.edit_testvar(p.config_id, Testvar(name='wanMode', value=v))

        # launch the package with wanMode=v
        print '   Launching package'
        j = c.jobs.launch(Job(package_id=p.id))

        # wait for job to be assigned a result ID
        while j.result_id is None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        print '        Result-ID: {0}'.format(j.result_id)
        print ''

    # restore original wanMode value in the package's config
    print '   Restoring original wanMode of {0}'.format(orig)
    print ''
    c.configs.edit_testvar(p.config_id, Testvar(name='wanMode', value=orig))

print 'done.'
