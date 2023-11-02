import logging as log
import datetime as dt
import os
import tkinter as tk
import ApiHandler as AH
# from tkinter import scrolledtext, simpledialog


class TkinterHandler:

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


    def mainScreen(self):
        self.Root = tk.Tk()
        self.Root.geometry('1280x720')
        self.Root.title('Dayz (Console) Manager')
        labelTitle = tk.Label(self.Root, text='Dayz (Console) Manager For Nitrado Hosted Servers', height=2)
        labelTitle.pack()
        if AH.ApiHandler.token != "" and AH.ApiHandler.token != None:
            self.openingBrowserToUrl()
        else:
            pass
        self.Root.mainloop()


    def apiErrorStartupScreen(self):
        ErrorWindow = tk.Tk()
        ErrorWindow.geometry('900x480')
        ErrorWindow.title('Dayz (Console) Manager')
        labelTitle = tk.Label(ErrorWindow, text='Nitrado is currently unavailable:', height=2)
        labelTitle.pack()
        ErrorWindow.mainloop()


    def openingBrowserToUrl(self):
        OpenedBrowser = tk.Tk()
        labelTitle = tk.Label(OpenedBrowser, text='Opening webbrowser,Please create a token and insert it here\n'
                                                  'this window will only open if you have not yet entered a key', height=2)
        labelTitle.pack()

        label = tk.Label(OpenedBrowser, text="Enter text:")
        label.pack()

        entry = tk.Entry(OpenedBrowser)
        entry.pack()

        get_input = entry.get()
        button = tk.Button(OpenedBrowser, text="Get Input", command=instApi.setToken(get_input))
        button.pack()



    def startProgram(self, a):
        if a == True:
            self.mainScreen()
        else:
            self.apiErrorStartupScreen()


instApi = AH.ApiHandler()