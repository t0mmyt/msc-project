#!/bin/bash
set -e

(cd /opt/code/render && python3 setup.py install)
(cd /opt/code/sax && python3 setup.py install)

python3 -m render
