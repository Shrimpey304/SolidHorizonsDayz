import logging as log
import datetime as dt
import os
import ApiHandler as AH
import TkinterHandler as TH
# import json as jsn
# import xmltodict
# import tkinter as tk

class Main:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'logs', f'Log_{log_time}.txt')
        log.basicConfig(
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )

    def uponStartup(self):
        if instApi.apiHealthCheck() == True:
            instTkint.startProgram()
        elif instApi.apiHealthCheck() == 1:
            print("starting")
        elif instApi.apiHealthCheck() == 2:
            print("not starting")


StartProgram = Main()
instApi = AH.ApiHandler()
instTkint = TH.TkinterHandler()

StartProgram.uponStartup()
