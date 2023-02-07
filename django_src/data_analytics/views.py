import os
import sys
from threading import Thread
from django.shortcuts import render
from django.http import HttpResponse
from .custom_src import parse_api as api # pylint: disable=import-error
from .custom_src import logger_config # pylint: disable=import-error
from .custom_src import analytics as an # pylint: disable=import-error

ui = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui_resources')
log_main = logger_config.log_app('main')

def data(request):
    return render(request, os.path.join(ui, 'data.html'))

def api_func(request):
    if api.api_check():
        try:
            Thread(target=api.proccessed_data_setup).start()
            Thread(target=api.rollover).start()
            Thread(target=api.auto_req).start()
            Thread(target=api.man_req).start()
            log_main.info('All threads started, app running')
            while True:
                user = input("Enter 'exit' to exit: ")
                if user == 'exit':
                    return api_func(request)
        except KeyError as error:
            log_main.error(error)
            sys.exit()

def type_func(request, date, data_type):
    return HttpResponse(an.Analytics.for_data(date=date, info_req=data_type))

def int_func(request, date):
    return HttpResponse(an.Analytics.inter_ac(date=date))
