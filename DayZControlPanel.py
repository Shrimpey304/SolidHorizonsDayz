import requests as rq
import logging as log
import datetime
import time
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import os
import json as jsn
import xmltodict

class tryNitrAPI:

    isLoggedInNitrado = False
    longlifekey = "Insert Token"


    def __init__(self):
        log_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Time to be set as file name
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'logs', f'Log_{log_time}.txt')
        self.serverXML_file_path = os.path.join(current_dir, 'Content', 'ServersXML', 'servers.xml')
        self.serverJSON_file_path = os.path.join(current_dir, 'Content', 'Data', 'servers.json')
        log.basicConfig(
            filename=log_file_path,
            level=log.DEBUG,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )
        self.create_ui_mainscreen()
        self.add_log_entry("Program started.")

    def add_log_entry(self, entry):
        self.log_console.config(state=tk.NORMAL)
        self.log_console.insert(tk.END, entry + "\n")
        self.log_console.config(state=tk.DISABLED)
        log.info(entry)

    def InitCheck(self):
        initialcheckURl = 'https://api.nitrado.net/ping'
        response = rq.get(initialcheckURl)
        JsonResponse = response.json()
        self.add_log_entry(str(JsonResponse))
        if JsonResponse['status'] == "success":
            self.add_log_entry("<Response [200]> starting program")
            self.StartProgram()
        else:
            self.add_log_entry("nitrado currently unavailable, please wait until nitrado is available")
            while True:
                print("nitrado currently unavailable, please wait until nitrado is available")
                time.sleep(2)

    def requireLogin(self):
        a=1

    def create_ui_mainscreen(self):
        self.root = tk.Tk()
        self.root.geometry('1280x720')
        self.root.title('Dayz (Console) Manager')
        labelTitle = tk.Label(self.root, text='Dayz (Console) Manager For Nitrado Hosted Servers', height=2)
        labelTitle.pack()
        self.log_console = scrolledtext.ScrolledText(self.root, height=10, width=50, wrap=tk.NONE)
        self.log_console.pack(expand=False, fill='none')
        self.log_console.config(xscrollcommand=self.log_console.xview, yscrollcommand=self.log_console.yview)
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.log_console.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        buttonToggleServerXML = tk.Button(self.root, text="Toggle server XML Text", command=self.toggle_xml_text)
        buttonToggleServerXML.pack(pady=10)
        self.text_widget = tk.Text(self.root)
        buttonGetAllServices = tk.Button(self.root, text="get all services", command=self.GetServiceInfo)
        buttonGetAllServices.pack(pady=10)
        self.servicetextwidget = tk.Text(self.root)

    def StartProgram(self):
        self.serversXMLtoJSON()
        self.root.mainloop()

    def open_textbox(self):
        InputServerXMl = simpledialog.askstring("Server FTP credentials", "Enter text:")
        if InputServerXMl:
            print("You entered:", InputServerXMl)

    def connectFTPtoNitradoserver(self):
        a = input('')

    def serversXMLtoJSON(self):
        with open(self.serverXML_file_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        json_data = jsn.dumps(data_dict)
        with open(self.serverJSON_file_path, "w") as json_file:
            json_file.write(json_data)

    def toggle_xml_text(self):
        if self.text_widget.winfo_ismapped():
            self.text_widget.pack_forget()  # Hide the text widget
        else:
            with open(self.serverXML_file_path, 'r') as file:
                data = file.read()
                self.add_log_entry("opened server ftp XML")
                self.text_widget.insert(tk.END, data)  # Insert text from the XML file
                self.text_widget.pack()  # Show the text widget

    def GetServiceInfo(self):
        if self.servicetextwidget.winfo_ismapped():
            self.servicetextwidget.pack_forget()  # Hide the text widget
        else:
            getallserviceurl = "https://api.nitrado.net/services"
            allserviceheaders = {'Authorization': self.longlifekey}
            serviceresponse = rq.get(getallserviceurl, headers=allserviceheaders)
            sresponseJson = serviceresponse.json()
            self.add_log_entry("opened userservices json")
            self.servicetextwidget.insert(tk.END, sresponseJson)  # Insert text from the XML file
            self.servicetextwidget.pack()  # Show the text widget

    def RestartService(self):
        restartserviceurl = f"https://api.nitrado.net/services/13885965/gameservers/restart" #still have to make this modifiable

tryinit = tryNitrAPI()
tryinit.InitCheck()
