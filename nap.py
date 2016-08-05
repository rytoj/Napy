#!/usr/bin/python3
import datetime
import sys
import time
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) # gets absolute Napy folder location
f = open(os.path.join(__location__, "chart.conf"))

# Handling command-line arguments



# color codes
class bcolors:
    DEFAULT = '\033[37m'
    OKBLUE = '\033[32m'
    WARNING = '\033[41m'
    ENDC = '\033[0m'


def get_list(config):
    '''
    Traverse config file
    Return Nap_list, as list
    '''
    Nap_list = []
    Nap_list = [item.rsplit() for item in config]
    format_time(Nap_list)
    return Nap_list

def format_time(datelist):
    '''
    Parsing list
    Returns parsed list
    '''
    for index, item in enumerate(datelist):
        if item[2].isnumeric() and item[4].isnumeric():
            h_start=item[2][:2]; m_start=item[2][2:]
            h_end=item[4][:2];   m_end=item[4][2:]
            if h_start.startswith("0"):
                h_start = h_start[-1]
            if m_start.startswith("0"):
                m_start = m_start[-1]
            if h_end.startswith("0"):
                h_end = h_end[-1]
            if m_end.startswith("0"):
                m_end = m_end[-1]
            datelist[index][2] =  {"hour":int(h_start), "minute": int(m_start)}
            datelist[index][4] =  {"hour":int(h_end), "minute":int(m_end)}
            #print("hour:", h_start ,"min:", m_start, "--to-- hour:", h_end ,"min:", m_end) #DEBUG
        else:
            return sys.exit("Error: Wrong format")


def cal_delta_to(hour, minute):
    '''
    Returns how many secons left until target time is reached
    '''
    now = datetime.datetime.now()
    #print("now:",now, "\nnow_slice:", now.timetuple()[0:3]) #DEBUG now: 2016-07-01 12:19:08.843500  now_slice: (2016, 7, 1)
    target = datetime.datetime(*now.timetuple()[0:3], hour, minute)
    # print("target:", target) #DEBUG
    if target < now:  # if the target is before now, add one day
        target += datetime.timedelta(days=1)
    diff = target - now
    return diff.seconds

def nap_time(h, m, hh, mm ):
    '''
    Returns nap time
    '''
    nap_starts = datetime.timedelta(hours=h, minutes=m)
    nap_ends = datetime.timedelta(hours=hh, minutes=mm)
    napt = nap_ends - nap_starts
    return napt

def sleep_print(verbose=0):
    '''
    prints informational text to terminal
    '''
    start_to_high = cal_delta_to(**Nap_list[0][2]) #pradinis nuo kurio lyginama, cal_delta_to(h,m) kaičiuoja kiek lieko sekundžiu iki to laiko
    if verbose == 1: print(Nap_list)
    if verbose == 1: print(Nap_list[0][2])
    for item in Nap_list:
        if verbose == 1: print(item[0], "from:", item[2], "Until:", item[4])
        sec_left = cal_delta_to(**item[2])
        if verbose == 1:
            print("{} or {} seconds, or {:.2f} minutes".format(str(datetime.timedelta(seconds=cal_delta_to(**item[2]))), cal_delta_to(**item[2]), cal_delta_to(**item[2])/60))

        if sec_left <= start_to_high:
            naptime = nap_time(item[2]['hour'],item[2]['minute'],item[4]['hour'],item[4]['minute'])
            start_to_high = sec_left # artimiausias miegas
    return str(datetime.timedelta(seconds=start_to_high)), naptime

def clear_screen():
    time.sleep(1)
    os.system("clear")

def nap_time_started(naptime):
    '''
    Function is executed when nape time is active
    '''
    nap_counter = int(naptime)
    while nap_counter > 0:
        print("Next closest nap: {color}{timeleft}{color_end} next naptime: {} ".format(nap, timeleft=rez, color=bcolors.OKBLUE, color_end=bcolors.ENDC))
        print("Nap ends afer:", datetime.timedelta(seconds=nap_counter))
        prints_sleep_conf()

        nap_counter -= 1
        nap_update()
        clear_screen()

def nap_update():
    '''
    Updates time variables
    '''
    rez, nap = sleep_print(verbose=0)
    leading_second = int(rez[-2]); seconds = int(rez[-1]) #defining time for checks
    hours = int(rez[0]); leading_min_zero = int(rez[2:3]); minutes = int(rez[3:4])
    # print(hours, leading_min_zero, minutes,leading_second, seconds, nap.seconds) #DEBUG
    global rez, nap, hours, leading_min_zero, minutes, leading_second, seconds


def prints_sleep_conf():
    for arg in sys.argv:
        if "-v" in arg:
            for nap in Nap_list:
                print("{:^4}: {:^2}:{:^2} - until - Hour: {}:{}".format(nap[0], nap[2]['hour'], nap[2]['minute'], nap[4]['hour'], nap[4]['minute']))
        else:
            pass

Nap_list = get_list(f)
os.system("clear")
while True:
    nap_update()

    if hours == 0 and leading_min_zero == 0 and minutes == 0 and leading_second == 0 and seconds == 0 : #printing nap time countdown
        nap_time_started(nap.seconds)

    if hours == 0 and minutes < 9 and leading_min_zero == 0:
        print("Closest nap: {color}{timeleft}{color_end} next naptime: {} ".format(nap, timeleft=rez, color=bcolors.WARNING, color_end=bcolors.ENDC))
        prints_sleep_conf()
    else:
        print("Closest nap: {color}{timeleft}{color_end} next naptime: {} ".format(nap, timeleft=rez, color=bcolors.OKBLUE, color_end=bcolors.ENDC))
        prints_sleep_conf()



    #TODO original for non linux
    #print("Closest nap: {} naptime: {} ".format(rez, nap))

    if rez == "0:05:00":
        os.system('notify-send "Napy" "5 minutes left"')
    if rez == "0:01:00":
        os.system('"espeak" "One minute left"')
    clear_screen()
