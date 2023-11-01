import requests as rq
import logging as log
import datetime as dt
import time
import os
# import json
# import xmltodict
# import tkinter as tk

class ApiHandler:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)  # gets path to the location of this file
        log_file_path = os.path.join(current_dir, 'Content', 'Logs', f'Log_{log_time}.txt')  # creates the full log path
        log.basicConfig(    # configures the log structure
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )

    def apiHealthCheck(self):    #checks if the nitrado services are working
        ApiHealthCheckUrl = "https://api.nitrado.net/ping"
        response = rq.get(ApiHealthCheckUrl)
        JsonResponse = response.json()
        if JsonResponse['status'] == "success":
            return True
        else:
            return False

    def apiMaintenanceCheck(self):
        a =1

