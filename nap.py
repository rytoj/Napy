#!/usr/bin/python3
import datetime
import sys
import time
import os

f = open("chart.conf")

def get_list(config):
    '''
    Traverse config file
    Return Nap_list, as list
    '''
    Nap_list = []
    for item in config:
        item = item.rsplit()
        Nap_list.append(item)
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
            # print("hour:", h_start ,"min:", m_start, "--to-- hour:", h_end ,"min:", m_end) #DEBUG
        else:
            return sys.exit("Error: Wrong format")


def cal_delta_to(hour, minute):
    '''
    Returns how many secons left until target time is reached
    '''
    now = datetime.datetime.now()
    # print("now:",now, "\nnow_slice:", now.timetuple()[0:3]) #DEBUG
    target = datetime.datetime(*now.timetuple()[0:3], hour, minute)
    # print("target:", target) #DEBUG
    if target < now:  # if the target is before now, add one day
        target += datetime.timedelta(days=1)
    diff = target - now
    return diff.seconds

def sleep_print(verbose=0):
    start_to_high = cal_delta_to(**Nap_list[0][2])
    for item in Nap_list:
        sec_left = cal_delta_to(**item[2])
        if verbose == 1:
            print("{} or {} seconds, or {} minutes".format(str(datetime.timedelta(seconds=cal_delta_to(**item[2]))), cal_delta_to(**item[2]), cal_delta_to(**item[2])/60))
        if sec_left < start_to_high:
            start_to_high = sec_left # artimiausias miegas
            # return print("Artimiausias Miegas po: {}".format(str(datetime.timedelta(seconds=start_to_high)))) #sustoja ties siuo elementu nes returnina
            return str(datetime.timedelta(seconds=start_to_high))



# print(Nap_list) #DEBUG
# print("----", Nap_list[2][2]) #DEBUG
# print("Total naps:", len(Nap_list)) #DEBUG
Nap_list = get_list(f)
os.system("clear")
while True:
    rez = sleep_print(verbose=0)
    print("Closest nap after: {}".format(rez))
    if rez == "0:05:00":
        os.system('notify-send "Napy" "5 minutes left"')
    time.sleep(1)
    os.system("clear")
