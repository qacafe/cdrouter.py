#!/usr/bin/env python3

import sys
import csv
import cdrouter



def usage():
    print()
    print('This script prints CDRouter test documentation in CSV format.')
    print()
    print('Usage: <base_url> <token> <expansion>')
    print('       <base_url> <token> "list" - List available expansions')
    print()

if len(sys.argv) < 4:
    usage()
    print()
    print(f'Error: not enough arguments')
    print()
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
group = sys.argv[3]

c = cdrouter.CDRouter(base, token=token)

expansions = [group.name for group in c.testsuites.list_groups()]

if group == 'list':
    print()
    print('Available expansions:')
    for exp in expansions:
        print(f'    "{exp}"')
    print()
    sys.exit(0)


if group not in expansions:
    usage()
    print(f'Error: unknown expansion "{group}"')
    print()
    sys.exit(1)


writer = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

writer.writerow(['Expansion', 'Module', 'Test', 'Synopsis', 'Description'])

for t in c.testsuites.list_tests(filter=f'group={group}', detailed=True):
    writer.writerow([t.group, t.module, t.name, t.synopsis, t.description])

