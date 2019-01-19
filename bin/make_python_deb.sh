#!/bin/bash 
#
#  Creates a .deb for a Python package, if it doesn't exist yet
#
#  Note - supposed to be run inside the docker installer container,
#  so /data has the source tree.
#
DEPENDENCY=$1
set -- $(echo $DEPENDENCY | sed 's/==/ /')
PACKAGE=$1
VERSION=$2
DEB=python-${PACKAGE}_${VERSION}

cd /data

if [ -f ${DEB}_*.deb ]
then
    echo $DEB already exists, skipping...
    exit 0
else
    fpm -s python -t deb $DEPENDENCY
fi

