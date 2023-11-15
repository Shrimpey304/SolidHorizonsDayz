import requests as rq
import logging as log
import datetime as dt
import TokenHandler as TKH
# import time
import os
import Utils
import json
# import xmltodict

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
        log.info("used apiHealthCheck()")
        ApiHealthCheckUrl = "https://api.nitrado.net/ping"
        response = rq.get(ApiHealthCheckUrl)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return True
        else:
            return False
        
    def apiMaintenanceCheck(self):
        log.info("used apiMaintenanceCheck()")
        apiHealthCheckUrl = "https://api.nitrado.net/maintenance"
        response = rq.get(apiHealthCheckUrl)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return decodedResponse['data']['maintenance']
        else:
            return "failed"
        
    
    def apiCheckTokenValidity(self):
        log.info("used apiCheckTokenValidity()")
        apiTokenValidatorUrl = "https://oauth.nitrado.net/token"
        apiTokenHeaders = {'Authorization': Utils.T}
        response = rq.get(apiTokenValidatorUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return True
        else:
            return False

    def apiCheckTokenOnLogin(self, key):
        log.info("used apiCheckTokenOnLogin()")
        try:
            apiTokenValidatorUrl = "https://oauth.nitrado.net/token"
            instTKH.tokenDecrypt(key)
            apiTokenHeaders = {'Authorization': Utils.T}
            response = rq.get(apiTokenValidatorUrl, headers=apiTokenHeaders)
            decodedResponse = response.json()
            if decodedResponse['status'] == "success":
                return True
            else:
                return False
        except ValueError as e:
            log.info(e)

        
    def apiFetchOwnerInfo(self):
        log.info("used apiFetchOwnerInfo")
        apiFetchOwnerInfoUrl = "https://api.nitrado.net/user"
        apiTokenHeaders = {'Authorization': Utils.T}
        response = rq.get(apiFetchOwnerInfoUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return decodedResponse['data']
        else:
            return "failed"
        
    def apiFetchAllOwnedServices(self):
        log.info("used apiFetchAllOwnedServices")
        apiFetchOwnedServicesUrl = "https://api.nitrado.net/services"
        apiTokenHeaders = {'Authorization': Utils.T}
        response = rq.get(apiFetchOwnedServicesUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return decodedResponse['data']
        else:
            return "failed"

    def apiRestartService(self, serviceID):
        response = None
        try:
            log.info("used apiRestartService")
            apiFetchRestartUrl = f"https://api.nitrado.net/services/{serviceID}/gameservers/restart"
            apiTokenHeaders = {'Authorization': Utils.T}
            response = rq.post(apiFetchRestartUrl, headers=apiTokenHeaders)
            decodedResponse = response.json()
            if decodedResponse['status'] == "success":
                return True
            else:
                return False
        except json.JSONDecodeError as json_error:
            log.info(f"JSON Decode Error: {json_error}")
            log.info(f"Response content: {response.content}")


    def apiStopService(self, serviceID):
        log.info("used apiRestartService")
        apiFetchStopUrl = f"https://api.nitrado.net/services/{serviceID}/gameservers/stop"
        apiTokenHeaders = {'Authorization': Utils.T}
        response = rq.post(apiFetchStopUrl, headers=apiTokenHeaders)
        decodedResponse = response.json()
        if decodedResponse['status'] == "success":
            return True
        else:
            return False

instTKH = TKH.TokenHandler()