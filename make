#!/bin/sh
cd `dirname $0`
. venvdailysummary/bin/activate
cd summary_maker
python3 entry.py $*
