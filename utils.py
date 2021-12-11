from os import listdir, system
from os.path import isfile, join
import time
import urllib.request
import json
from datetime import date, timedelta

def format_time(t_sec):
    if t_sec < 60:
        return str(round(t_sec, 1)) + ' seconds left (estimate)'
    elif t_sec < 3600:
        return str(round(t_sec/60, 1)) + ' minutes left (estimate)'
    else:
        return str(round(t_sec/3600, 1)) + ' hours left (estimate)'

class TrackProgress:
    def __init__(self):
        self.perc_last_check = 0
        self.time_last_check = 0

    def check(self, perc):
        if ( time.time() - self.time_last_check ) > 3:
            delta_perc = perc - self.perc_last_check
            delta_time = time.time() - self.time_last_check

            current_perc_per_second = delta_perc/delta_time
            perc_left = 100 - perc

            if current_perc_per_second == 0:
                print('too early to make an estimate')
                return
            sec_left = perc_left / current_perc_per_second
            time_left_estimate = format_time(sec_left)
            self.perc_last_check = perc
            self.time_last_check = time.time()
            
            system('cls')
            print(str(round(perc, 1)) + ' %')
            print(time_left_estimate)

def getFilesInDir(dir_path):
    onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    return onlyfiles

def getJsonFromURL(url, timeToWait=1):
    print('downloading ' + url + '...')

    req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Personal script'
            }
        )
    with urllib.request.urlopen(req) as url_page:
        pageJson = json.loads(url_page.read().decode('utf-8'))

        time.sleep(timeToWait)

        return pageJson

def get_list_of_past_dates(nDays):
    dates = []

    new_date = date.today()
    timedelta_day = timedelta(days=1)

    for i in range(nDays):
        new_date = new_date - timedelta_day
        dates.append(new_date.strftime("%Y-%m-%d"))

    return dates

def call_and_retry(func, numAttempts, wait_times, *args, **kwargs):
    '''
    Calls 'func' and, if it raises an exception, retries 'numAttempts' times.
    Arguments:
        - func: the function to call
        - numAttempts: how many attempts to make before raising the exception.
                       If numAttempts == -1: keep trying forever.
        - wait_times: a list of numbers. If an exception occurs, it waits the number of seconds specified here.
                      For example wait_times = [3, 6, 9] means that it will wait 3 seconds, then 6, then 9 for all the remaining attempts.
        - args and kwargs: the arguments to pass to func()
    '''
    import time
    import traceback

    attempts = 0
    while True:
        try:
            ret = func(*args, **kwargs)
            return ret
        except:
            print('error in function ' + str(func.__name__) + ':')
            print(traceback.format_exc())

            attempts += 1
            if attempts >= numAttempts and numAttempts != -1:
                raise

            wait_time = wait_times[min(attempts-1, len(wait_times)-1)]
            print('waiting ' + str(wait_time) + ' second(s) and retrying...')
            time.sleep( wait_time )



