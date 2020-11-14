from tkinter import *
import time
import pygame


class mainmenu(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        pygame.mixer.init()
        self.controller = controller
        self.configure(bg="#bdc3c7")
        self.timer_img=PhotoImage(file=r"Favorites/timer.png")
        self.stopwatch_img=PhotoImage(file=r"Favorites/stopwatch.png")
        self.detect_img=PhotoImage(file=r"Favorites/detect.png")
        self.music_img=PhotoImage(file=r"Favorites/music.png")
        self.musicstop_img=PhotoImage(file=r"Favorites/musicstop.png")
        self.mode = "STOP"
        self.draw_frame()
    
    def draw_frame(self):
        self.grid_rowconfigure(1, weight=1)
        self.top_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.middle_frame = Frame(self,width=320,height=200,bg="#bdc3c7")
        self.bottom_frame = Frame(self,width=320,height=150,bg="#bdc3c7")
        self.bottom_btn_frame = Frame(self,width=320,height=100,bg="#bdc3c7")

        self.top_frame.grid(row=0,sticky="ew")
        self.middle_frame.grid(row=1,sticky="ew")
        self.bottom_btn_frame.grid(row=3,sticky="ew")
        self.bottom_frame.grid(row=4,sticky="ew")
        self.draw_button()

    
    def draw_button(self):
        btn_stopwatch = Button(self.bottom_btn_frame,image=self.stopwatch_img,activebackground="#dfe6e9",text="스톱워치",compound="top",bg="#bdc3c7",relief="flat",command=lambda:self.controller.show_frame('stopwatch'))
        btn_timer     = Button(self.bottom_btn_frame,image=self.timer_img,activebackground="#dfe6e9",bg="#bdc3c7",text="타이머",compound="top",relief="flat",command=lambda:self.controller.show_frame('Timer'))
        #btn_camera     = Button(self.bottom_btn_frame,image=self.detect_img,activebackground="#dfe6e9",bg="#bdc3c7",text="감시모드",compound="top",relief="flat",command=lambda:self.controller.show_frame('Camera'))
        self.clock_label = Label(self.middle_frame, text="00:00:00",font=("Helvetica",40),fg="#2c3e50",bg="#bdc3c7")
        self.btn_music   = Button(self.top_frame,image=self.music_img,activebackground="#dfe6e9",bg="#bdc3c7",relief="flat",command=self.music_control)
        self.vol = Scale(self.top_frame,from_=0.0,to=1.0,orient=HORIZONTAL,resolution = 0.1,command=self.change_volume,bg="#bdc3c7")

        self.vol.grid(row=0,column=1)
        self.clock_label.grid(row=0,rowspan=10,sticky="nsew",padx=8)
        self.btn_music.grid(row=0,sticky="nw",padx=10,pady=10)
        btn_stopwatch.grid(row=0,column=2,padx=23)
        btn_timer.grid(row=0,column=1,padx=23)
        #btn_camera.grid(row=0,column=3,padx=23)
        self.clock()
    def clock(self):
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        am_pm = time.strftime("%p")

        self.clock_label.config(text= hour + ":" + minute + ":" + second + " " + am_pm) 
        self.clock_label.after(1000,self.clock)
    def music_control(self):
        if self.mode == "STOP":
            self.mode = "RUNNING"
            self.btn_music.config(image=self.musicstop_img)
            self.music_start()
        elif self.mode == "RUNNING":
            self.mode = "STOP"
            self.btn_music.config(image=self.music_img)
            self.music_start()
    def music_start(self):
        if self.mode == "RUNNING":
            self.play_music()
        elif self.mode == "STOP":
            pygame.mixer.music.stop()
            
    def play_music(self):
        pygame.mixer.music.load(r"music/rain.wav")
        pygame.mixer.music.play(-1)
    def change_volume(self,volume):
        pygame.mixer.music.set_volume(self.vol.get())
    
