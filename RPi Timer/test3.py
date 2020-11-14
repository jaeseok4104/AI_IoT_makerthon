from tkinter import *
import os
print(os.path.dirname(os.path.realpath(__file__)))
root = Tk()
root.title('Model Definition')
root.geometry('{}x{}'.format(320, 410))
root.grid_rowconfigure(1,weigh=1)
root.configure(bg="#bdc3c7")
#root.grid_columnconfigure(0,weigh=1)
timer_img=PhotoImage(file=r"Favorites/timer.png")
stopwatch_img=PhotoImage(file=r"Favorites/stopwatch.png")
detect_img=PhotoImage(file=r"Favorites/detect.png")
music_img=PhotoImage(file=r"Favorites/music.png")

#timer_img1 = timer_img.subsample(1,1)
#stopwatch_img1 = stopwatch_img.subsample(1,1)
#detect_img1 = detect_img.subsample(1,1)
#프레임 생성
top_frame = Frame(root,width=320,height=50,bg="#bdc3c7")
middle_frame = Frame(root,width=320,height=200,bg="#bdc3c7")
bottom_frame = Frame(root,width=320,height=150,bg="#bdc3c7")
bottom1_frame = Frame(root,width=320,height=100,bg="#bdc3c7")

#프레임 배치
top_frame.grid(row=0,sticky="ew")
middle_frame.grid(row=1,sticky="ew")
bottom1_frame.grid(row=3,sticky="ew")
bottom_frame.grid(row=4,sticky="ew")
#버튼 생성
music_btn = Button(top_frame,image=music_img,bg="#bdc3c7",relief="flat")
clock_lbl  = Label(middle_frame,font=("Helvetica",40),fg="#2c3e50",bg="#bdc3c7",text="00:00:00 AM")
timer_btn = Button(bottom1_frame,image=timer_img,bg="#bdc3c7",text="타이머",compound="top",relief="flat")
stopwatch_btn = Button(bottom1_frame,image=stopwatch_img,text="스톱워치",compound="top",bg="#bdc3c7",relief="flat")
camera_btn = Button(bottom1_frame,image=detect_img,bg="#bdc3c7",text="감시모드",compound="top",relief="flat")
#스크롤바
volume =0.0
var = DoubleVar()
scale = Scale(top_frame,variable=var,orient = HORIZONTAL, from_ = 0.0,to=1.0,resolution=0.1,bg="#bdc3c7",relief="flat")
scale.grid(row=0,column=3)
print (volume)
#버튼 배치
music_btn.grid(row=0,sticky="nw",padx=10,pady=10)
clock_lbl.grid(row=0,rowspan=10,sticky="nsew",padx=8)
timer_btn.grid(row=0,column=1,padx=23)
stopwatch_btn.grid(row=0,column=2,padx=23)
camera_btn.grid(row=0,column=3,padx=23)
root.mainloop()