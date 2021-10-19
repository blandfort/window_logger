# Window Logger

This repository contains code to log information about active windows
(on a linux machine).


## Usage

### Run Manually

Run the logger using `python3 run.py`.
(Only standard python packages are used, so it is normally not
necessary to create a virtual environment.)

For running the logger as background job, run `python3 run.py &`.

### Run Automatically

If you wish to run the logger in the background every time
your machine boots, you can do so by creating a cron job:

1. `crontab -e`
2. Add the line `@reboot python3 /path/to/this/repo/run.py &`
4. (Optional) Check if crontab is properly configured by running `crontab -l`
