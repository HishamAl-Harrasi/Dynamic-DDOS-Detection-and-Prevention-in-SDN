#!/bin/sh

sudo apt-get install mininet

sudo mn -c

sudo apt-get install git

git clone git://github.com/mininet/mininet

cd mininet

git tag # list available versions

git checkout -b Lastversion

cd ..

sudo PYTHON=python3 mininet/util/install.sh -n   # install Python 3 Mininet
# Or if you need the Python2 version of mininet:
# sudo PYTHON=python2 mininet/util/install.sh -n   # install Python 2 Mininet

sudo mn
