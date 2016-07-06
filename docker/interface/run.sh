#!/bin/bash
set -e

(cd /opt/code/interface && python3 setup.py clean --all && python3 setup.py install)

python3 -m interface
