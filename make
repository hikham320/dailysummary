#!/bin/sh
cd `dirname $0`
. venv/bin/activate
cd summary_maker
python3 entry.py $*
