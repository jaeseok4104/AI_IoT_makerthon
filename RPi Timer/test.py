from tkinter import *

root = Tk()
root.title('Model Definition')
root.geometry('{}x{}'.format(320, 480))
root.configure(bg="#bdc3c7")


speech_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\musicstop.png")
start_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\start.png")
reset_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\reset.png")
back_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\back.png")
up_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\up.png")
down_img=PhotoImage(file=r"C:\Users\seong yuel chun\Desktop\TimerApp\Favorites\down.png")
down_img=down_img.subsample(2,2)
up_img=up_img.subsample(2,2)
speech_img=speech_img.subsample(2,2)
#프레임 생성
top_frame = Frame(root,width=320,height=50,bg="red")
upset_frame = Frame(root,width=320,height=50,bg="#bdc3c7")
clock_frame = Frame(root,width=320,height=50,bg="#bdc3c7")
downset_frame = Frame(root,width=320,height=50,bg="#bdc3c7")
btn_frame = Frame(root,width=320,height=50,bg="#bdc3c7")
back_frame = Frame(root,width=320,height=150,bg="#bdc3c7")

#프레임 배치
top_frame.grid(row=0,sticky="ew",pady=20)
upset_frame.grid(row=1,sticky="ew")
clock_frame.grid(row=2,sticky="ew")
downset_frame.grid(row=3,sticky="ew")
btn_frame.grid(row=4,sticky="ew",pady=20)
back_frame.grid(row=5,sticky="ew",pady=80)

#버튼 생성
speech_btn = Button(top_frame,image=speech_img,activebackground="#dfe6e9",bg="#bdc3c7",relief="flat")
clock_lbl  = Label(clock_frame,font=("Helvetica",60),fg="#2c3e50",bg="#bdc3c7",text="00:00:00")
up1_btn = Button(upset_frame,image=up_img,bg="#bdc3c7",relief="flat",width=93)
up2_btn = Button(upset_frame,image=up_img,bg="#bdc3c7",relief="flat",width=93)
up3_btn = Button(upset_frame,image=up_img,bg="#bdc3c7",relief="flat",width=93)
down1_btn = Button(downset_frame,image=down_img,bg="#bdc3c7",relief="flat",width=95)
down2_btn = Button(downset_frame,image=down_img,bg="#bdc3c7",relief="flat",width=95)
down3_btn = Button(downset_frame,image=down_img,bg="#bdc3c7",relief="flat",width=95)
start_btn = Button(btn_frame,image=start_img,bg="#bdc3c7",relief="flat")
reset_btn = Button(btn_frame,image=reset_img,bg="#bdc3c7",relief="flat")
back_btn = Button(back_frame,image=back_img,bg="#bdc3c7",relief="flat")
#버튼 배치

speech_btn.grid(row=0,column=0,padx=10)
up1_btn.grid(row=0,column=0)
up2_btn.grid(row=0,column=1,padx=9)
up3_btn.grid(row=0,column=2)
down1_btn.grid(row=0,column=0)
down2_btn.grid(row=0,column=1,padx=9)
down3_btn.grid(row=0,column=2)
clock_lbl.grid(row=0,padx=3)
start_btn.grid(row=0,column=1,padx=70)
reset_btn.grid(row=0,column=2)
back_btn.grid(row=0,column=0)

root.mainloop()