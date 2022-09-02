#!/usr/bin/env python

#
# This script launches all packages with a specified tag on a given CDRouter
# system. After the packages have completed, the script creates an XML report in
# JUnit format that Gitlab can parse. The script also downloads each test's log
# and capture files to be stored as artifacts using Gitlab's CI/CD
# infrastructure. All created files are stored in out/ and can be saved as
# artifacts in the Gitlab CD/CD test job.
#
# Example job in a .gitlab-ci.yaml file:
#
#   cdrouter-test:
#     tags:
#       - cdrouter-gitlab-runner
#     stage: test
#     script:
#       - gitlab.py <CDRouter-URL> <token> nightly $CI_COMMIT_BRANCH,$CI_PIPELINE_ID
#     artifacts:
#       when: always
#       paths:
#         - out/*.zip
#       reports:
#         junit: out/results_*.xml
#
import sys
import time
import shutil
import os

from zipfile import ZipFile
from cdrouter import CDRouter
from cdrouter.jobs import Job
from cdrouter.jobs import Options

if len(sys.argv) < 5:
    print('usage: <base_url> <token> <run-tag> <result-tag>')
    print('       <base_url>    URL of CDRouter system')
    print('       <token>       CDRouter system API token')
    print('       <run-tag>     All packages with this tag will be launched')
    print('       <result-tag>  Results will be tagged with this tag or tags in a comma separated list')
    sys.exit(1)

base = sys.argv[1]
token = sys.argv[2]
tag_name = sys.argv[3]
result_tags = sys.argv[4]

result_tags_list = result_tags.split(",")
# create service
c = CDRouter(base, token=token)

packages = c.packages.iter_list(filter=['tags@>{'+tag_name+'}'])
jobs = [Job(package_id=p.id, options=Options(tags=result_tags_list)) for p in packages]

fails = 0
# launch all packages
for j in c.jobs.bulk_launch(jobs=jobs):
    while j.result_id is None:
        time.sleep(1)
        j = c.jobs.get(j.id)
    print('Test package launched. Result-ID: {0}'.format(j.result_id))
    print('Waiting for job to complete...')

    u = c.results.updates(j.result_id, None)
    while u:
        r = c.results.get(j.result_id)
        if r.status in ['completed', 'stopped', 'error']:
            break
        time.sleep(1)
        u = c.results.updates(j.result_id, u.id)

    result_url = base.strip('/') + '/results/' + str(r.id)
    print('Job status: {0}'.format(r.status))

    if r.status != 'completed':
        print('Error: test package "{0}" did not complete successfully ({1})'.format(r.package_name, r.status))
        print('Test report: {0}'.format(result_url))
        fails = 1

    print('Test results:')
    print('')
    print('{0:>15} : {1}'.format('Summary',      r.result))
    print('{0:>15} : {1}'.format('Start',        r.created))
    print('{0:>15} : {1}'.format('Duration',     r.duration))
    print('{0:>15} : {1}'.format('Package',      r.package_name))
    print('{0:>15} : {1}'.format('Config',       r.config_name))
    print('{0:>15} : {1}'.format('Tags',         r.tags))
    print('{0:>15} : {1}'.format('Pass',         r.passed))
    print('{0:>15} : {1}'.format('Fail',         r.fail))
    print('')
    print('{0:>15} : {1}'.format('Test Report',  result_url))
    print('{0:>15} : {1}'.format('Test Summary', result_url + '/print'))
    print('')

    cwd = os.getcwd()
    results_directory = os.path.join(cwd,'out')
    os.mkdir(results_directory)
    os.chdir(results_directory)
    file_name_suffix = result_tags.replace(",","-")
    filename = 'results_{0}_{1}.xml'.format(j.result_id, file_name_suffix)
    print('Writing results to file "{0}" in JUnit XML format'.format(filename))
    with open(filename, 'w') as f:
        # Junit format for test suite
        f.write('<testsuite name="CDRouter" package="{0}" failures="{1}" tests="{2}">\n'.format(r.package_name, r.fail, r.tests))
        for t in c.tests.iter_list(j.result_id):
            url='{0}/results/{1}/tests/{2}'.format(base, j.result_id, t.seq)
            if t.name == 'start' or t.name == 'final':
                continue

            # Download & zip log and capture files
            zip_file_name = t.name + '.zip'
            with ZipFile(zip_file_name, mode='w') as archive:
                with open(t.log, 'w') as logFile:
                    logFile.write(c.tests.get_log_plaintext(t.id, t.seq))
                    logFile.close()
                    archive.write(t.log)
                    os.remove(t.log)

                    for caps in c.captures.list(t.id, t.seq):
                        b,capFileName = c.captures.download(t.id, t.seq, caps.interface)
                        with open(capFileName, 'wb') as capFile:
                            shutil.copyfileobj(b,capFile)
                        capFile.close()
                        archive.write(capFileName)
                        os.remove(capFileName)
            archive.close()

            # Junit format for testcase
            f.write('    <testcase name="{0}" classname="{1}" file="{2}" time="{3}">\n'.format(t.name+": "+t.description, r.package_name, url, t.duration))

            if t.result in ['fail', 'fatal']:
                f.write('        <failure message="test failures">\n')
                f.write('View the full CDRouter test log {0}\n'.format(url))

                logs = c.tests.list_log(t.id, t.seq, filter=['prefix=FAIL'], limit='100000')
                for l in logs.lines:
                    f.write('FAIL: {0}\n'.format(l.message))
                f.write('        </failure>\n')
            elif t.result in ['pending', 'skipped']:
                f.write('        <skipped/>\n')
            f.write('    </testcase>\n')
        f.write('</testsuite>\n')
    f.close()

    if r.fail > 0:
        fails = 1

    os.chdir(cwd)
exit(fails)
