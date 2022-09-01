#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

from os import environ
from os.path import basename
import tarfile
from time import sleep, time

import docker
from docker.errors import ImageNotFound
import pytest

from cdrouter import CDRouter

@pytest.fixture(name="cdrouter")
def my_cdrouter():
    client = docker.from_env()

    try:
        client.images.get(environ.get('CDR_DOCKER_IMAGE'))
    except ImageNotFound:
        client.images.pull(environ.get('CDR_DOCKER_IMAGE'))

    volumes = None
    if 'CDR_DOCKER_VOLUMES' in environ:
        volumes = environ.get('CDR_DOCKER_VOLUMES').split(',')

    container = client.containers.create(
        environ.get('CDR_DOCKER_IMAGE'),
        auto_remove=True, tty=True, privileged=True,
        publish_all_ports=True,
        volumes=volumes)
    container.start()

    info = docker.APIClient().inspect_container(container.id)

    ip = info['NetworkSettings']['Gateway']
    port = info['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
    base = 'http://{}:{}'.format(ip, port)
    c = CDRouter(base)
    port_https = info['NetworkSettings']['Ports']['443/tcp'][0]['HostPort']
    base_https = 'https://{}:{}'.format(ip, port_https)
    c_https = CDRouter(base_https, insecure=True)

    ok = False
    exit_code = 3
    timeout = time() + 10
    while ok is False and time() < timeout:
        (exit_code, _) = container.exec_run(['/usr/cdrouter/etc/cdrouter.sh', 'status'])
        if exit_code == 0:
            ok = True
            break
        sleep(0.5)
    if ok is False:
        raise ValueError('unable to start cdrouter')

    ok = False
    timeout = time() + 10
    while ok is False and time() < timeout:
        try:
            c.system.time()
            ok = True
            break
        except: # pylint: disable=bare-except
            sleep(0.5)
    if ok is False:
        raise ValueError('unable to connect to cdrouter')

    yield {
        'container':  container,
        'ip':         ip,
        'port':       port,
        'base':       base,
        'c':          c,
        'port_https': port_https,
        'base_https': base_https,
        'c_https':    c_https
    }

    container.stop(timeout=0)

@pytest.fixture(name="c")
def my_c(cdrouter):
    yield cdrouter['c']

@pytest.fixture(name="c_https")
def my_c_https(cdrouter):
    yield cdrouter['c_https']

def import_all_from_file(c, path, replace_existing=True):
    with open(path, 'rb') as fd: # pylint: disable=unspecified-encoding
        imp = c.imports.stage_import_from_file(fd)
    impreq = c.imports.get_commit_request(imp.id)
    impreq = should_import_all(impreq, replace_existing=replace_existing)
    return c.imports.commit(imp.id, impreq)

def should_import_all(impreq, replace_existing=True):
    impreq.replace_existing = replace_existing
    for x in impreq.configs:
        impreq.configs[x].should_import = True
    for x in impreq.devices:
        impreq.devices[x].should_import = True
    for x in impreq.packages:
        impreq.packages[x].should_import = True
    for x in impreq.results:
        impreq.results[x].should_import = True
    return impreq

@pytest.fixture(name="copy_file_from_container")
def my_copy_file_from_container(tmp_path):
    tmp_path = str(tmp_path)

    def _my_copy_file_from_container(container, path):
        (exit_code, output) = container.exec_run(['/bin/sh', '-c', 'ls {}'.format(path)])
        assert exit_code == 0
        lspath = output.decode().strip()
        base = basename(lspath)

        bits, _ = container.get_archive(lspath)

        local_path = '{}/{}'.format(tmp_path, 'files.tar')
        with open(local_path, 'wb') as fd: # pylint: disable=unspecified-encoding
            for chunk in bits:
                fd.write(chunk)

        with tarfile.open(local_path, mode='r') as tar:
            tar.extractall(path=tmp_path)

        return '{}/{}'.format(tmp_path, base)
    return _my_copy_file_from_container

@pytest.fixture(name="copy_file_to_container")
def my_copy_file_to_container(tmp_path):
    tmp_path = str(tmp_path)

    def _my_copy_file_to_container(container, path):
        tarpath = '{}/{}'.format(tmp_path, 'files.tar')

        with tarfile.open(tarpath, 'w') as tar:
            tar.add(path, arcname=basename(path))

        dstpath = '/tmp'

        with open(tarpath, 'rb') as fd: # pylint: disable=unspecified-encoding
            container.put_archive(dstpath, fd)

        return '{}/{}'.format(dstpath, basename(path))

    return _my_copy_file_to_container
