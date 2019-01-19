#
#  a Makefile for non pythoneers
#
#  Note - invoke with "gnumake".
#

.PHONY: all test clean dev dist Dockerfile docker

PACKAGER_DOCKER=registry.ecg.so/shared.python-dist:14.04-1
VERSION:=$(shell python setup.py --version)

all:
	python setup.py build


test:
	python setup.py test


clean:
	python setup.py clean
	rm -rf *.deb build *.egg-info dist requirements.txt .eggs


dev:
	# Note - develop in a virtual env!
	python setup.py develop --upgrade
	pip freeze | grep -v 'esindexer' >requirements.txt


dist: dev all test
	# Package dependencies
	docker run -i -t --rm -v ${PWD}:/data ${PACKAGER_DOCKER} /bin/bash -xc 'cd /data; cat requirements.txt | while read p; do /data/bin/make_python_deb.sh $$p;done'
	# Package this
	docker run -i -t --rm -v ${PWD}:/data ${PACKAGER_DOCKER} /bin/bash -xc "cd /data; fpm -s python -t deb -v ${VERSION} setup.py"


dist-test:
	docker run -i -t --rm -v ${PWD}:/data ${PACKAGER_DOCKER} /bin/bash


install:
	python setup.py install

