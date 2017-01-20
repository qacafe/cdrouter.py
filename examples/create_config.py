#!/usr/bin/env python

import sys

from cdrouter import CDRouter
from cdrouter.configs import Config

if len(sys.argv) < 3:
    print('usage: <base_url> <token>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]

# create service
c = CDRouter(base, token=token)

cfg = c.configs.create(Config(
    name='My Config File',
    contents="""
testvar lanIp 192.168.1.1
testvar lanMask 255.255.255.0
"""))

print('New config has ID {}'.format(cfg.id))
