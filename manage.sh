#!/bin/bash

function ssh-config {
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cp -p ${SSH_DIR}/* ~/.ssh
    chown -R $(id -un):$(id -gn) ~/.ssh
}

function git-config {
    git config --global user.email "${GIT_USER_EMAIL}" > /dev/null 2>&1
    git config --global user.name "${GIT_USER_NAME}" > /dev/null 2>&1
}

function setup {
    requirements
    install-editable
}

function requirements {
    pip install --no-cache-dir -r requirements.txt
    pip install --no-cache-dir twine
}

function install {
    pip install .
}

function install-editable {
    pip install -e .
}

function publish {
    bump
    build
    push
}

function bump {
    previousVersion=$( grep '^__version__ =' cdrouter/__init__.py | sed 's/__version__ = \"\(.*\)\"/\1/' )
    echo "Next version number? (previous: '$previousVersion')"
    read version

    if [ "$version" = "" ];
    then
        echo "No version number entered, aborting bump"
        exit 1
    fi

    sed -i -b "s/__version__ = .*/__version__ = \"$version\"/" cdrouter/__init__.py
}

function clean {
    rm -rf build cdrouter.egg-info dist
}

function build {
    clean
    python setup.py sdist bdist_wheel
}

function push {
    echo "Break (Ctrl+c) or type 'abort' and hit enter if something is wrong. Else, press enter"
    read foobar

    if [ "$foobar" = "abort" ];
    then
        echo "User entered 'abort', aborting push"
        exit 1
    fi

    twine upload dist/*

    git commit -am "Publish version $version"

    git tag -m "Version $version" v$version

    git push --tags origin master
}

while [[ $# -ne 0 ]];
do
    $1
    shift
done
