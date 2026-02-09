#!/usr/bin/env python

import sys
from cdrouter import CDRouter

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <testvar>')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
testvar = sys.argv[3]

# create service
c = CDRouter(base, token=token)

for cfg in c.configs.iter_list():
    print('==========================')
    print(f'Config Name: "{cfg.name}"')
    all_testvars = c.configs.list_testvars(cfg.id)
    tvs = [tv for tv in all_testvars if tv.name == testvar]
    for t in tvs:
        for name, value in t.__dict__.items():
            print(f'{name:15} = {value}')
        print()
