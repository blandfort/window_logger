#!/bin/bash

# We need to set some environment variables to give cron jobs
# access to the GUI session
# (See https://unix.stackexchange.com/a/547212)
export DISPLAY=':0'
export XAUTHORITY='/home/john/.Xauthority'

python3 /home/john/code/logging/windows/run.py &
