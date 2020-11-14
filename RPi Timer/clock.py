from tkinter import *

import time
import wave
import serial
from pygame import mixer
from Mainmenu import mainmenu
from StopWatch import stopwatch
from Timer import Timer
from CameraStopWatch import Camera

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Productivity Time")
        self.geometry("320x440+0+0")
        self.resizable(0,0)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (mainmenu, Timer, stopwatch,Camera):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('mainmenu')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

ser = serial.Serial('/dev/ttyACM0', 115200)

a = App()
a.mainloop()