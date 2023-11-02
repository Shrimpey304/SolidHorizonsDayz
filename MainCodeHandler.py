import logging as log
import datetime as dt
import os
import ApiHandler as AH
import TkinterHandler as TH
import webbrowser as wb
# import json as jsn
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
                instTkint.startProgram(True)
            elif instApi.apiHealthCheck() != "failed":
                instTkint.startProgram(False)
            else:
                instTkint.startProgram(False)
        except Exception as e:
            log.info(e)
            print(e)
            
    def browserOpenNitradoTokenPage(self):
        url = "https://server.nitrado.net/eng/developer/tokens"
        wb.open_new(url)



StartProgram = Main()
instApi = AH.ApiHandler()
instTkint = TH.TkinterHandler()

StartProgram.uponStartup()
