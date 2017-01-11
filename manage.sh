#!/bin/bash

function publish {
    bump
    build
    push
}

function bump {
    previousVersion=$( grep '^__version__ =' cdrouter/__init__.py | sed 's/__version__ = \"\(.*\)\"/\1/' )
    echo "Next version number? (previous: '$previousVersion')"
    read version
    sed -i -b "s/__version__ = .*/__version__ = \"$version\"/" cdrouter/__init__.py
}

function build {
    rm -rf build cdrouter.egg-info dist
    python setup.py sdist bdist_wheel
}

function push {
    echo "Break (Ctrl+c) here if something is wrong. Else, press enter"
    read foobar

    twine upload dist/*

    git commit -am "Publish version $version"

    git tag -m "Version $version" v$version

    git push origin master
    git push --tags
}

$1
