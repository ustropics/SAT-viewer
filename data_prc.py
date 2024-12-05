from imports import *
from config import *

def create_main_dict(sidebar):
    start_time = sidebar[2].value
    end_time = sidebar[3].value

    main_dict['start_time'] = start_time
    main_dict['end_time'] = end_time

def create_timerange_dict():
    start_time = main_dict['start_time']
    end_time = main_dict['end_time']

