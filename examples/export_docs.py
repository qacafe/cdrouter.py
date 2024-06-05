#!/usr/bin/env python3

import sys
import csv
import cdrouter



def usage():
    print()
    print('usage: <base_url> <token> <extension>')
    print()
    print('extensions:')
    print('  "Apple HomeKit", BBF.069, CDRouter, DOCSIS, IKE, IPv6,')
    print('  Multiport, Performance, SNMP, Security, Storage,')
    print('  TR-069, USP, Custom')
    print()

if len(sys.argv) < 4:
    usage()
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
ext = sys.argv[3]

extensions = ['Apple HomeKit', 'BBF.069', 'CDRouter', 'DOCSIS', 'IKE', 'IPv6',
              'Multiport', 'Performance', 'SNMP', 'Security', 'Storage',
              'TR-069', 'USP', 'Custom']

if ext not in extensions:
    print(f'Error: unknown extension "{ext}"\n')
    usage()
    sys.exit(1)


c = cdrouter.CDRouter(base, token=token)

writer = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

writer.writerow(['Extension', 'Module', 'Test_Name', 'Synopsis', 'Description'])

for t in c.testsuites.list_tests(filter=f'group={ext}', detailed=True):
    writer.writerow([t.group, t.module, t.name, t.synopsis, t.description])

