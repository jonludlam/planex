#!/usr/bin/env bash

set -xe

cd ..
mkdir SPECS
ln -s ../planex/planex.spec SPECS/planex.spec
planex/docker/wrap.sh planex-init
planex/docker/wrap.sh planex-pin add SPECS/planex.spec planex#HEAD
mkdir mock
ln -s /etc/mock/default.cfg mock/
ln -s /etc/mock/logging.ini mock/
planex/docker/wrap.sh make
