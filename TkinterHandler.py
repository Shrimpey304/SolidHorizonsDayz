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
                log.info("Token/key combination correct, heading to mainscreen")
                logscreen.destroy()
                self.mainScreen()
            else:
                if TkinterHandler.UsedLabelLoginError < 1:
                    log.info("Token/key combination incorrect")
                    LoginErrorLabel = tk.Label(logscreen, text='your passkey was incorrect, please restart the program'
                                                               ' or empty the Credentials.Json to Restart the registration process', height=2)
                    LoginErrorLabel.pack(pady=5)
                    TkinterHandler.UsedLabelLoginError += 1

        def renewToken():
            log.info("invalidating token, going to register screen")
            instTKH.invalidateToken()
            logscreen.destroy()
            self.openingBrowserToUrl()


        logscreen = tk.Tk()
        logscreen.geometry('900x480')
        LoginScreenLabel = tk.Label(logscreen, text='please provide the key that was given on entering the token', height=2)
        LoginScreenLabel.pack(pady=5)
        entry = tk.Entry(logscreen)
        entry.pack(pady=5)
        LogInButton = tk.Button(logscreen, text="Log in", command=loginValid)
        LogInButton.pack(pady=5)
        LogInButton = tk.Button(logscreen, text="Renew the token (this will delete your current token off the system)", command=renewToken)
        LogInButton.pack(pady=5)
        logscreen.mainloop()


    def mainScreen(self):
        ServicesList = ["---"]
        ServicesIDs = []
        SelectedServices = []

        def getServices(gs):
            ServicesList.clear()
            ServicesIDs.clear()
            SelectedServices.clear()
            log.info("Cleared all lists")

            ServicesList.append("---")
            if gs:
                log.info("allowed 'All' services")
                ServicesList.append('All')
            for services in instApi.apiFetchAllOwnedServices()['services']:
                ServicesList.append(f'{services["details"]["name"]} - {services["id"]}')
                ServicesIDs.append(services["id"])
            try:
                if not gs and 'All' in ServicesList:
                    log.info("Disallowed 'All' services")
                    ServicesList.remove('All')
                else:
                    pass
                setSelectedServiceID()
                log.info(f'Set selected server(s) to {SelectedServices}')
                updateOptionMenu()
            except ValueError as e:
                log.info(f"currently expected error: {e}")

        def isTicked():
            checkbox_state = SelectAllCheckboxVar.get()
            if checkbox_state:
                getServices(True)
            else:
                getServices(False)

        def updateOptionMenu():
            menu = option_menu["menu"]
            menu.delete(0, "end")
            for service in ServicesList:
                menu.add_command(label=service, command=tk._setit(selected_option, service))

        def setSelectedServiceID():
            selected = selected_option.get()
            if selected == 'All':
                for s in ServicesIDs:
                    if s not in SelectedServices:
                        SelectedServices.append(s)
                # selectedServices.remove('All')
            else:
                SelectedServices.append(selected)
            log.info(f"Selected Services:{SelectedServices}")

        self.Root = tk.Tk()
        self.Root.geometry('1280x720')
        self.Root.title('Dayz (Console) Manager')
        labelTitle = tk.Label(self.Root, text='Dayz (Console) Manager For Nitrado Hosted Servers', height=2)
        labelTitle.grid(row=0, column=5, padx=10, pady=10)

        WelcomeUserLabel = tk.Label(self.Root, text=f'welcome {instApi.apiFetchOwnerInfo()["user"]["username"]}')
        WelcomeUserLabel.grid(row=1, column=0, padx=10, pady=10)

        label = tk.Label(self.Root, text="Select an option:")
        label.grid(row=2, column=0, padx=10, pady=10)

        # Create a variable to store the selected option
        selected_option = tk.StringVar(self.Root)
        selected_option.set(ServicesList[0])  # Set the default option

        SelectAllCheckboxVar = tk.BooleanVar(self.Root)
        SelectAllCheckbox = tk.Checkbutton(self.Root, text="Allow 'all' services", variable=SelectAllCheckboxVar,
                                           command=isTicked)
        SelectAllCheckbox.grid(row=2, column=2, padx=10, pady=10)

        option_menu = tk.OptionMenu(self.Root, selected_option, *ServicesList)
        option_menu.grid(row=2, column=1, padx=10, pady=10)

        isTicked()  # Call isTicked to initially populate the options

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

        log.info(f"unable to start program: \n\t\t\t\t{cloudStatus()}\n\t\t\t\t{domainStatus()}\n\t\t\t\t{dnsStatus()}\n\t\t\t\t{pmacctStatus()}")

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
            log.info("opening browser to token page")
            url = "https://server.nitrado.net/eng/developer/tokens"
            wb.open_new(url)

        def get_input_and_set_token():
            log.info("getting and encrypting token")
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
        log.info("Showing key to user")
        def copyKey():
            pyperclip.copy(Utils.K)

        def toMainScreen():
            ShowKey.destroy()
            self.mainScreen()

        ShowKey = tk.Tk()
        ShowKey.geometry('400x280')

        if instApi.apiCheckTokenValidity() == True:
            log.info("Token is Valid")
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
        log.info("Starting program")
        if a == True:
            self.mainScreen()
        else:
            self.apiErrorStartupScreen()


instApi = AH.ApiHandler()
instTKH = TKH.TokenHandler()

