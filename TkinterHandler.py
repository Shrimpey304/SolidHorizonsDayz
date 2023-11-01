import logging as log
import datetime as dt
import os
import tkinter as tk
# from tkinter import scrolledtext, simpledialog


class TkinterHandler:

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

    def mainScreen(self):
        self.root = tk.Tk()
        self.root.geometry('1280x720')
        self.root.title('Dayz (Console) Manager')
        self.root.mainloop()
        a = input()

    def startProgram(self):
        self.mainScreen()
