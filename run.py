import re
import os
import subprocess
import time
import json
import datetime
import logging


# Window information is collected according to the following interval
# (in seconds):
DEFAULT_INTERVAL = 10

# Window information is stored in a logfile according to that path:
DEFAULT_LOGFILE = os.path.join(os.path.dirname(__file__), "windows.log")


def get_active_window_info():
    """Find information about the currently active window, using xprop."""
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    logging.debug(stdout)
    logging.debug(stderr)

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)

        if window_id==b"0x0":
            return None

        window = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    info = {}
    for line in stdout.split(b'\n'):
        match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", line)
        if match is not None:
            info['title'] = match.group("name").strip(b'"').decode('utf-8')
            logging.debug("Title found: %s" % info["title"])

        match = re.match(b"WM_CLASS\(\w+\) = (?P<class>.+)$", line)
        if match is not None:
            info['class'] = match.group("class").decode('utf-8').replace('"', '') #.strip(b'"')
            logging.debug("Class found: %s" % info["class"])

    if len(info):
        return info
    else:
        return None


#TODO make it possible to change default settings by passing command line args
if __name__=="__main__":
    debug_log = os.path.join(os.path.dirname(__file__), "debug.log")
    logging.basicConfig(filename=debug_log, level=logging.DEBUG)

    start_time = time.time()
    while True:
        logging.debug("Writing active window information to file '%s' ..." % DEFAULT_LOGFILE)

        with open(DEFAULT_LOGFILE, 'a') as f:
            f.write(datetime.datetime.now().isoformat() + '\t')
            f.write(json.dumps(get_active_window_info()))
            f.write('\n')

        next_time = time.time()

        # Make sure that we log according to specified interval
        passed_time = next_time - start_time
        sleep_time = max(DEFAULT_INTERVAL - passed_time, 0)
        time.sleep(sleep_time)

        start_time = time.time()
