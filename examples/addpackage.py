#!/usr/bin/env python3


#
# CDRouter addpackage.py
# Copyright 2017, QA Cafe
#
# This script will go through a list of CDRouter systems,
# and for each system, generate a list of unique configs
# used by packages owned by a given user for that system.
# For each of these configs, a new package will be created
# based on a list of tests/modules.  The new packages will
# be owned by the provided user.  
#
# Multiple packages created on the same system will be given
# suffixes, beginning with "_2", "_3", etc.
#
# The user for the new packages must already exist on each
# system.  Also, if a package by the same name already exists
# on the system, it is not touched.
#
# The list of tests comes from a text file, one entry per line.
# Entries can be individual tests or entire test modules,
# e.g., MODULE_apps.tcl
#
# The list of systems comes from another text file, one entry per line.
# The format is:
# URL	username	password
# Each username will be used to create the list of unique
# configs for that system (the owner of the package those configs use).
#
# Optional arguments allow:
# * Adding tags to the new packages
# * Prompting the user before creating each package
# * Launching each new package, returning a job_id


import argparse
import sys
import os
import re
from cdrouter import CDRouter
from cdrouter.cdrouter import CDRouterError
from cdrouter.filters import Field as field
from cdrouter.packages import Package
from cdrouter.jobs import Job

# Max file size to read from.
MAX_FILE_SIZE          = 1024 * 1024

# Deal with command line options.
parser = argparse.ArgumentParser(description='Add package(s) to CDRouter system(s).')
parser.add_argument('package_name', help='The name of the package(s) to be created.  Multiple packages created on the same system will contain numerical suffixes, e.g., "_2", "_3", etc.')
parser.add_argument('package_owner', help='The owner of the package(s) to be created.  The user must already exist on the system(s).')
parser.add_argument('tests', help='The name of a file containing a list of tests and/or modules to define the package(s), one entry per line.  Modules can be specified as well, e.g., MODULE_apps.tcl')
parser.add_argument('cdrsystems', help='The name of a file containing the list of CDRouter systems, one entry per line, three fields separated by whitespace: <URL> <username> <password>.  Each username will be used to create the list of unique configs for that system (the owner of the package those configs use).')

parser.add_argument('-t', '--tags', help='A comma separated list of tags to be added to the package.')
parser.add_argument('-p', '--prompt', action='store_true', help='Prompt before creating a package.')
parser.add_argument('-r', '--run', action='store_true', help='Launch the package after creating it.  A job_id will be returned.')

args = parser.parse_args()

# Read the contents of args.tests.
tests = []
if os.path.isfile(args.tests):
    statinfo = os.stat(args.tests)
    if statinfo.st_size > MAX_FILE_SIZE:
        print('{} is too big'.format(args.tests))
        sys.exit(1)
    try:
        with open(args.tests) as f:
            lines = f.readlines()
            f.close()
    except IOError as e:
        print('Cannot open {}, {}'.format(args.tests, e))
        sys.exit(1)
    else:
        for line in lines:
            tests.append(line.strip())

# Read the contents of args.cdrsystems.
cdrsystems = []
if os.path.isfile(args.cdrsystems):
    statinfo = os.stat(args.cdrsystems)
    if statinfo.st_size > MAX_FILE_SIZE:
        print('{} is too big'.format(args.cdrsystems))
        sys.exit(1)
    try:
        with open(args.cdrsystems) as f:
            lines = f.readlines()
            f.close()
    except IOError as e:
        print('Cannot open {}, {}'.format(args.cdrsystems, e))
        sys.exit(1)
    else:
        i = 0
        for line in lines:
            i += 1
            fields = line.split()
            if len(fields) != 3:
                print('Wrong number of fields in {}, line {}'.format(args.cdrsystems, i))
                sys.exit(1)
            cdrsystem = {'url': fields[0], 'username': fields[1], 'password': fields[2]}
            cdrsystems.append(cdrsystem)

# Here we go...
for cdrsystem in cdrsystems:

    print()
    print('{}'.format(cdrsystem['url']))
    print('=========================')
    print()

    cdr = CDRouter(cdrsystem['url'], username=cdrsystem['username'], password=cdrsystem['password'], retries=1)

    # Do a sanity check that we can talk to this cdrsystem.
    try:
        cdr.system.time()
    except CDRouterError as ce:
        print('Cannot connect to {}, {}'.format(cdrsystem['url'], ce))
        continue

    # Get the user_id for the user that will own the new package(s).
    try:
        user_id = cdr.users.get_by_name(args.package_owner).id
    except CDRouterError as ce:
        print('Cannot get info for user {}, {}'.format(args.package_owner, ce))
        continue

    # Get the user_id for the existing package owner.
    try:
        existing_package_owner_id = cdr.users.get_by_name(cdrsystem['username']).id
    except CDRouterError as ce:
        print('Cannot get info for user {}, {}'.format(cdrsystem['username'], ce))
        continue

    # Get a set of unique configs for all packages owned by this user
    config_ids = []
    try:
        packages = cdr.packages.iter_list(filter=[field('user_id').eq(existing_package_owner_id)])
        for package in packages:
            if package.config_id not in config_ids:
                config_ids.append(package.config_id)
    except CDRouterError as ce:
        print('Cannot get a list of packages owned by {}, {}'.format(cdrsystem['username'], ce))
        continue

    # For each config, create a new package.
    count = 0
    for config_id in config_ids:

        # Generate the new package name.
        count += 1
        package_name = args.package_name
        if count > 1:
            package_name += '_' + str(count)

        # Get the name of the config we'll be using.
        try:
            config_name = cdr.configs.get(config_id).name
        except CDRouterError as ce:
            print('Cannot get info about config {}'.format(config_id))
            continue

        print('Creating new package "{}" owned by "{}" using config "{}"'.format(package_name, args.package_owner, config_name)) 

        # Prompt the user if requested.
        if args.prompt:
            prompt = None
            while prompt != 'y' and prompt != 'n':
                prompt = input('OK? (y/n) ')
            if prompt == 'n':
                continue

        # See if a package with that name already exists.  If so, leave it alone and move on.
        try:
            cdr.packages.get_by_name(package_name)
        except CDRouterError as ce:
            pass
        else:
            print('A package with this name already exists.  Skipping...')
            continue

        # Create the new package.
        kwargs = {'name': package_name, 'description': 'Created by addpackage', 'testlist': tests, 'user_id': user_id, 'config_id': config_id}
        if args.tags != None:
            kwargs['tags'] = re.split(',', args.tags)
        try:
            package = cdr.packages.create(Package(**kwargs))
        except CDRouterError as ce:
            print('Cannot create package, {}'.format(ce))
            continue

        # Run the package if requested.
        if args.run:
            kwargs = {'package_id': package.id, 'user_id': user_id}
            try:
                job = cdr.jobs.launch(Job(**kwargs))
            except CDRouterError as ce:
                print('Cannot launch package, {}'.format(ce))
                continue

            print('job_id = {}'.format(job.id))
