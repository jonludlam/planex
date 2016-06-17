#!/bin/sh -xe

docker build -t planex-release:0.7.3 --no-cache --rm=true --force-rm -f Dockerfile.release .
docker build -t planex-master --no-cache --rm=true --force-rm -f Dockerfile.master .
docker build -t planex-unstable --no-cache --rm=true --force-rm -f Dockerfile.unstable .
