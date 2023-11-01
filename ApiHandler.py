import requests as rq
import logging as log
import datetime as dt
import time
import os
import json
# import xmltodict
# import tkinter as tk

class ApiHandler:
    
    token  = "Insert Token Here"
    
    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)  # gets path to the location of this file
        log_file_path = os.path.join(current_dir, 'Content', 'logs', f'Log_{log_time}.txt')  # creates the full log path
        log.basicConfig(    # configures the log structure
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )



    def apiHealthCheck(self):    #checks if the nitrado services are working
        ApiHealthCheckUrl = "https://api.nitrado.net/ping"
        response = rq.get(ApiHealthCheckUrl)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return True
        else:
            return False
        
    def apiMaintenanceCheck(self):
        apiHealthCheckUrl = "https://api.nitrado.net/maintenance"
        response = rq.get(apiHealthCheckUrl)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return decodedResponse['data']['maintenance']
        else:
            return "failed"
        
    
    def apiCheckTokenValidity(self):
        apiTokenValidatorUrl = "https://oauth.nitrado.net/token"
        apiTokenHeaders = {'Authorization': self.token}
        response = rq.get(apiTokenValidatorUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return True
        else:
            return False
        
    def apiFetchOwnerInfo(self):
        apiFetchOwnerInfoUrl = "https://api.nitrado.net/user"
        apiTokenHeaders = {'Authorization': self.token}
        response = rq.get(apiFetchOwnerInfoUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return decodedResponse['data']
        else:
            return "failed"
        
        
peeperpooper = ApiHandler()
print(peeperpooper.apiFetchOwnerInfo())