import logging as log
import datetime as dt
import os
import ApiHandler as AH
import TkinterHandler as TH
import json
# import xmltodict
# import tkinter as tk

class Main:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Logs', f'Log_{log_time}.txt')
        log.basicConfig(
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )

    def uponStartup(self):
        try:
            if instApi.apiHealthCheck() == True:

                with open('Content/Credentials/Credentials.json') as json_file:
                    CredJSON = json.load(json_file)

                if CredJSON['token'] is None or CredJSON['token'] == "":
                    log.info("no token found, redirecting to set a token")
                    instTkint.openingBrowserToUrl()
                else:
                    log.info("Key accepted, logging in user")
                    instTkint.loginScreen()

            elif instApi.apiHealthCheck() != "failed":
                log.info("api healthcheck failed, unable to start program")
                instTkint.startProgram(False)
            else:
                log.info("api healthcheck failed, unable to start program")
                instTkint.startProgram(False)

        except Exception as e:
            log.info(f"error?:{e}")


StartProgram = Main()
instApi = AH.ApiHandler()
instTkint = TH.TkinterHandler()

StartProgram.uponStartup()
