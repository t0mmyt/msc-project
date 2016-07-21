#!/bin/bash
set -e
alias python3=/usr/bin/python3

(cd /opt/code/interface && python3 setup.py clean --all && python3 setup.py install)

python3 -m interface
