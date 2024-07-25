#!/usr/bin/env python

import argparse
from datetime import datetime
import os
import re
import sys

from cdrouter import CDRouter
from cdrouter.cdrouter import CDRouterError
from cdrouter.filters import Field as field

parser = argparse.ArgumentParser(description='''

This script will copy resources between CDRouter systems.


All resource types will be copied unless the '--resources' argument is used:
    eg: '--resources configs,packages' will copy only configs and packages


You may also specify a date range with '--after' and/or '--before':
    '--after 2024-01-01 --before 2024-03-31'


Resources that already exist wil NOT be copied unless '--overwrite' is used.
    * Importing a result will automatically import config/device/package it references

    * Adding the --overwrite flag will overwrite the result, but not
      the referenced config/device/package

    * When importing a package, the same rule applies to the referenced config/device

''', formatter_class=argparse.RawDescriptionHelpFormatter)

def valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid date: "{s}".'
        raise argparse.ArgumentTypeError(msg)

parser.add_argument('src_base', metavar='SRC', help='Base URL of CDRouter source system')
parser.add_argument('dst_base', metavar='DST', help='Base URL of CDRouter destination system')

parser.add_argument('--src-token', metavar='STR', help='API token to use with source CDRouter system', default=None)
parser.add_argument('--dst-token', metavar='STR', help='API token to use with destination CDRouter system', default=None)

parser.add_argument('--src-user', metavar='STR', help='Username to use with source CDRouter system', default=None)
parser.add_argument('--src-password', metavar='STR', help='Password to use with source CDRouter system', default=None)

parser.add_argument('--dst-user', metavar='STR', help='Username to use with destination CDRouter system', default=None)
parser.add_argument('--dst-password', metavar='STR', help='Password to use with destination CDRouter system', default=None)

parser.add_argument('--insecure', help='Allow insecure HTTPS connections', action='store_true', default=False)
parser.add_argument('--overwrite', help='Overwrite existing resources on destination CDRouter system', action='store_true', default=False)
parser.add_argument('--resources', metavar='LIST', help='Comma-separated list of resource types to migrate (default: %(default)s)', type=str, default='configs,devices,packages,results')

parser.add_argument('--after', metavar='DATE', help='Migrate only resources created after this date (format: YYYY-MM-DD)', type=valid_date, default=None)
parser.add_argument('--before', metavar='DATE', help='Migrate only resources created before this date (format: YYYY-MM-DD)', type=valid_date, default=None)

parser.add_argument('--verbose', help='Enable verbose output', action='store_true', default=False)

args = parser.parse_args()

def print_verbose(msg):
    if args.verbose:
        print(msg)

def migrate(src, dst, resource, name_or_id, filter, should_import_rtypes):
    resources = f'{resource}s'
    src_service = getattr(src, resources)
    dst_service = getattr(dst, resources)


    for r in src_service.iter_list(filter=filter, sort='-created'):
        try:
            staged = None

            if not args.overwrite:
                dst_item = None
                dst_name = r.id

                try:
                    if name_or_id == 'id':
                        dst_item = dst_service.get(r.id)
                    elif name_or_id == 'name':
                        dst_name = r.name
                        dst_item = dst_service.get_by_name(r.name)
                except CDRouterError as cde:
                    pass


                if dst_item != None:
                    print_verbose('Skipping {resource} {dst_name}, already exists')
                    continue

            url = f'{args.src_base.rstrip("/")}/{resources}/{r.id}/'
            staged = dst.imports.stage_import_from_url(url, token=src.token, insecure=args.insecure)
            impreq = dst.imports.get_commit_request(staged.id)

            impreq.replace_existing = True
            should_import = False

            for rtype in should_import_rtypes:
                rs = getattr(impreq, rtype)
                for name in rs:
                    if args.overwrite or rs[name].existing_id == None:
                        rs[name].should_import = True
                        if rtype == resources:
                            should_import = rs[name].should_import

            if not should_import:
                print_verbose(f'Skipping {resource} {r.id}')
                dst.imports.delete(staged.id)
                continue

            impreq = dst.imports.commit(staged.id, impreq)

            rs = getattr(impreq, resources)
            for name in rs:
                if not rs[name].should_import:
                    continue
                if rs[name].response.imported:
                    print(f'Imported {resource} {name}')
                else:
                    print(f'Error importing {resource} {name}: {rs[name].response.message}')
        except CDRouterError as cde:
            print(f'Error migrating {resource} {r.id}: {cde}')
            if staged != None:
                dst.imports.delete(staged.id)



src = CDRouter(args.src_base, token=args.src_token, username=args.src_user, password=args.src_password, insecure=args.insecure)
dst = CDRouter(args.dst_base, token=args.dst_token, username=args.dst_user, password=args.dst_password, insecure=args.insecure)

resources = args.resources.split(',')


filter = []
if args.after != None:
    filter.append(field('created').gt(args.after))
if args.before != None:
    filter.append(field('created').lt(args.before))

if 'results' in resources:
    print('\nTransferring results')
    migrate(src, dst, 'result', 'id', filter, ['results'])

if 'packages' in resources:
    print('\nTransferring packages')
    migrate(src, dst, 'package', 'name', filter, ['configs', 'devices', 'packages'])

if 'configs' in resources:
    print('\nTransferring configs')
    migrate(src, dst, 'config', 'name', filter, ['configs'])

if 'devices' in resources:
    print('\nTransferring devices')
    migrate(src, dst, 'device', 'name', filter, ['devices'])

