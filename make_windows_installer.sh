#!/bin/sh
set -x
python setup.py bdist_wininst  --install-script postinstall.py
