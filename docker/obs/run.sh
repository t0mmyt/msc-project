#!/bin/bash
set -e

(cd /opt/code/tsdatastore && python3 setup.py install)
(cd /opt/code/observation && python3 setup.py install)

python3 -m observation
