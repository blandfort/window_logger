import re
import subprocess
import time
import json
import datetime
import logging


# Window information is collected according to the following interval
# (in seconds):
DEFAULT_INTERVAL = 10

# Window information is stored in a logfile according to that path:
DEFAULT_LOGFILE = "windows.log"


def get_active_window_info():
    """Find information about the currently active window, using xprop."""
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    info = {}
    for line in stdout.split(b'\n'):
        match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", line)
        if match is not None:
            info['title'] = match.group("name").strip(b'"').decode('utf-8')

        match = re.match(b"WM_CLASS\(\w+\) = (?P<class>.+)$", line)
        if match is not None:
            info['class'] = match.group("class").decode('utf-8').replace('"', '') #.strip(b'"')

    if len(info):
        return info
    else:
        return None


#TODO make it possible to change default settings by passing command line args
if __name__=="__main__":
    start_time = time.time()
    while True:
        #logging.info("Writing active window information to file '%s' ..." % DEFAULT_LOGFILE)
        with open(DEFAULT_LOGFILE, 'a') as f:
            f.write(datetime.datetime.now().isoformat() + '\t')
            f.write(json.dumps(get_active_window_info()))
            f.write('\n')

        next_time = time.time()

        # Make sure that we log according to specified interval
        passed_time = next_time - start_time
        sleep_time = max(DEFAULT_INTERVAL - passed_time, 0)
        time.sleep(sleep_time)

        start_time = next_time
