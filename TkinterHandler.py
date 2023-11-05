import logging as log
import datetime as dt
import os
import tkinter as tk
import ApiHandler as AH
import TokenHandler as TKH
import Utils
import pyperclip
import webbrowser as wb
from PIL import Image, ImageTk
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

    UsedLabelLoginError = 0
    def loginScreen(self):

        def loginValid():
            get_input = entry.get()
            if instApi.apiCheckTokenOnLogin(get_input) == True:
                self.mainScreen()
            else:
                if TkinterHandler.UsedLabelLoginError < 1:
                    LoginErrorLabel = tk.Label(logscreen, text='your passkey was incorrect, please restart the program'
                                                               ' or empty the Credentials.Json to Restart the registration process', height=2)
                    LoginErrorLabel.pack(pady=5)
                    TkinterHandler.UsedLabelLoginError += 1

        logscreen = tk.Tk()
        logscreen.geometry('900x480')
        LoginScreenLabel = tk.Label(logscreen, text='please provide the key that was given on entering the token', height=2)
        LoginScreenLabel.pack(pady=5)
        entry = tk.Entry(logscreen)
        entry.pack(pady=5)
        button = tk.Button(logscreen, text="Log in", command=loginValid)
        button.pack(pady=5)
        logscreen.mainloop()


    def mainScreen(self):
        self.Root = tk.Tk()
        self.Root.geometry('1280x720')
        self.Root.title('Dayz (Console) Manager')
        labelTitle = tk.Label(self.Root, text='Dayz (Console) Manager For Nitrado Hosted Servers', height=2)
        labelTitle.pack(pady=5)
        WelcomeUserLabel = tk.Label(self.Root, text=f'welcome {instApi.apiFetchOwnerInfo()["user"]["username"]}')
        WelcomeUserLabel.pack(padx=10, pady=10, anchor='w')
        self.Root.mainloop()

    def apiErrorStartupScreen(self):
        def cloudStatus():
            if instApi.apiMaintenanceCheck()["cloud_backend"]:
                return "cloud : maintenance\n"
            else:
                return "cloud : online\n"

        def domainStatus():
            if instApi.apiMaintenanceCheck()["domain_backend"]:
                return "domain : maintenance\n"
            else:
                return "domain : online\n"

        def dnsStatus():
            if instApi.apiMaintenanceCheck()["dns_backend"]:
                return "dns : maintenance\n"
            else:
                return "dns : online\n"

        def pmacctStatus():
            if instApi.apiMaintenanceCheck()["pmacct_backend"]:
                return "pmacct : maintenance\n"
            else:
                return "pmacct : online\n"
        ErrorWindow = tk.Tk()
        ErrorWindow.geometry('900x480')
        ErrorWindow.title('Dayz (Console) Manager')
        labelTitle = tk.Label(ErrorWindow, text='Nitrado is currently unavailable:', height=2)
        labelTitle.pack(pady=5)
        labelStatus = tk.Label(ErrorWindow, text=f'Status: \n'f'{cloudStatus()}{domainStatus()}{dnsStatus()}{pmacctStatus()}')
        labelStatus.pack()
        image = Image.open("Content/Images/ApiError.png")
        photo = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(ErrorWindow, image=photo)
        imageLabel.pack()
        ErrorWindow.mainloop()


    def openingBrowserToUrl(self):

        Used = False

        def browserOpenNitradoTokenPage():
            url = "https://server.nitrado.net/eng/developer/tokens"
            wb.open_new(url)

        def get_input_and_set_token():
            get_input = entry.get()
            global Used
            Used = True
            self.OpenedBrowser.destroy()
            instTKH.tokenEncrypt(get_input)
            self.showKey()

        if Used == False:
            self.OpenedBrowser = tk.Tk()  # Use Toplevel instead of tk.Tk()
            self.OpenedBrowser.geometry('400x280')
            labelTitle = tk.Label(self.OpenedBrowser, text='Opening webbrowser, Please create a token and insert it here\n'
                                                      'This window will only open if you have not yet entered a key', height=2)
            labelTitle.pack()
            label = tk.Label(self.OpenedBrowser, text="Enter text:", width=6)
            label.pack(pady=5)
            entry = tk.Entry(self.OpenedBrowser)
            entry.pack(pady=5)
            button = tk.Button(self.OpenedBrowser, text="Get Input", command=get_input_and_set_token)
            button.pack(pady=5)
            OpenBrowserButton = tk.Button(self.OpenedBrowser, text="Open the key page", command=browserOpenNitradoTokenPage)
            OpenBrowserButton.pack(pady=5)
            self.OpenedBrowser.mainloop()
        else:
            pass

        self.showKey()

    def showKey(self):

        def copyKey():
            pyperclip.copy(Utils.K)

        def toMainScreen():
            ShowKey.destroy()
            self.mainScreen()

        ShowKey = tk.Tk()
        ShowKey.geometry('400x280')

        if instApi.apiCheckTokenValidity() == True:
            LabelTitle = tk.Label(ShowKey, text='This is your login key, SAVE THIS CAREFULLY:', height=2)
            LabelTitle.pack(pady=5)
            LabelKey = tk.Label(ShowKey, text=f'{Utils.K}')
            LabelKey.pack(pady=5)

            CopyKeyButton = tk.Button(ShowKey, text="Copy key to clipboard", command=copyKey)
            CopyKeyButton.pack(pady=5)
            ToMainButton = tk.Button(ShowKey, text="Head to Mainscreen", command=toMainScreen)
            ToMainButton.pack(pady=5)
        else:
            def retToShowBrowser():
                ShowKey.destroy()
                self.openingBrowserToUrl()

            LabelTitle = tk.Label(ShowKey, text='The Token you have entered is not a valid token,'
                                                ' please try again with a freshly generated token')
            LabelTitle.pack(pady=5)
            TryAgainButton = tk.Button(ShowKey, text="Try again", command=retToShowBrowser)
            TryAgainButton.pack(pady=5)

    def startProgram(self, a):
        if a == True:
            self.mainScreen()
        else:
            self.apiErrorStartupScreen()


instApi = AH.ApiHandler()
instTKH = TKH.TokenHandler()

