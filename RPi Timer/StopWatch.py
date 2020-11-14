from tkinter import *

class stopwatch(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.configure(bg="#bdc3c7")
        self.controller = controller
        self.mode = "STOP"
        self.start_img=PhotoImage(file=r"Favorites/start.png")
        self.pause_img=PhotoImage(file=r"Favorites/pause.png")
        self.resume_img=PhotoImage(file=r"Favorites/resume.png")
        self.reset_img=PhotoImage(file=r"Favorites/reset.png")
        self.back_img=PhotoImage(file=r"Favorites/back.png")
        self.draw_frame()
    def draw_frame(self):
        self.top_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.clock_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.btn_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.back_frame = Frame(self,width=320,height=150,bg="#bdc3c7")


        self.top_frame.grid(row=0,sticky="ew",pady=50)
        self.clock_frame.grid(row=1,sticky="ew")
        self.btn_frame.grid(row=2,sticky="ew")
        self.back_frame.grid(row=3,sticky="ew",pady=120)
        self.draw_button()
    def draw_button(self):    
        self.btn_control=Button(self.btn_frame,image=self.start_img,activebackground="#dfe6e9",bg="#bdc3c7",relief="flat",command = self.change_control)
        self.btn_reset=Button(self.btn_frame,image=self.reset_img,activebackground="#dfe6e9",bg="#bdc3c7",relief="flat",command = self.time_reset)
        btn_back=Button(self.back_frame,image=self.back_img,activebackground="#dfe6e9",bg="#bdc3c7",relief="flat",command=lambda:self.controller.show_frame("mainmenu"))
        self.label_time=Label(self.clock_frame,text="00:00:00",font=("Helvetica",60),bg="#bdc3c7",fg="#2c3e50")
        
        self.label_time.grid(row=0,padx=3) #여기 padx 값 수정 <-x-> 가 padx 값임
        self.btn_control.grid(row=0,column=0,padx=70)#여기도 그냥 padx 값 보이는거 다 수정해야해 
        self.btn_reset.grid(row=0,column=1)# stopwatch나 timer나 다
        btn_back.grid(row=0,column=0)#
    
    
    
    def change_control(self):
        if self.mode == "STOP":
            self.mode = "RUNNING"
            print(self.mode)
            self.stopwatch_start()
        elif self.mode == "RUNNING":
            self.mode = "PAUSE"
            print(self.mode)
        elif self.mode == "PAUSE":
            self.mode = "RUNNING"
            print(self.mode)
        self.change_button()
    
    def change_button(self):
        if self.mode == "STOP":
            self.btn_control.config(image=self.start_img)
        elif self.mode == "RUNNING":
            self.btn_control.config(image=self.pause_img)
        elif self.mode == "PAUSE":
            self.btn_control.config(image=self.resume_img)
        
    def stopwatch_start(self):
        self.stopwatch_loop(0)
    
    def stopwatch_loop(self,s):
        hour , second = divmod(s,3600)
        minute , second = divmod(second,60)

        if self.mode == "RUNNING":
            new_time = "{:02}:{:02}:{:02}".format(hour, minute, second)
            s += 1
            self.label_time.config(text=new_time)
        elif self.mode == "STOP":
            return
        self.label_time.after(1000,self.stopwatch_loop,s)

        

    def time_reset(self):
        self.mode = "STOP"
        self.label_time.config(text="00:00:00")
        self.change_button()