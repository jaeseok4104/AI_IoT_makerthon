#from __future__ import division

import time
import re
import sys
from tkinter import *
from pygame import mixer
#from google.cloud import speech
#from google.cloud.speech import enums
#from google.cloud.speech import types
#import pyaudio
#from six.moves import queue


"""
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
class MicrophoneStream(object):
    Opens a recording stream as a generator yielding the audio chunks.
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        Continuously collect data from the audio stream, into the buffer.
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
"""

class Timer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="#bdc3c7")
        self.controller = controller
        mixer.init()
        self.sp_timer = []
        self.sp_hour = 0
        self.sp_min = 0
        self.sp_sec = 0
        self.mode = "STOP"
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.start_img=PhotoImage(file=r"Favorites/start.png")
        self.pause_img=PhotoImage(file=r"Favorites/pause.png")
        self.resume_img=PhotoImage(file=r"Favorites/resume.png")
        self.reset_img=PhotoImage(file=r"Favorites/reset.png")
        self.back_img=PhotoImage(file=r"Favorites/back.png")
        self.speech_img=PhotoImage(file=r"Favorites/speech.png")
        up_img=PhotoImage(file=r"Favorites/up.png")
        down_img=PhotoImage(file=r"Favorites/down.png")
        self.down_img=down_img.subsample(2,2)
        self.up_img=up_img.subsample(2,2)
        self.draw_frame()
    def draw_frame(self):
        self.top_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.upset_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.clock_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.downset_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.btn_frame = Frame(self,width=320,height=50,bg="#bdc3c7")
        self.back_frame = Frame(self,width=320,height=150,bg="#bdc3c7")

        
        self.top_frame.grid(row=0,sticky="ew",pady=20)
        self.upset_frame.grid(row=1,sticky="ew")
        self.clock_frame.grid(row=2,sticky="ew")
        self.downset_frame.grid(row=3,sticky="ew")
        self.btn_frame.grid(row=4,sticky="ew",pady=20)
        self.back_frame.grid(row=5,sticky="ew",pady=70)
        self.draw_button()
    def draw_button(self):    
        self.btn_control=Button(self.btn_frame,image=self.start_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",command = self.change_control)
        self.btn_reset=Button(self.btn_frame,image=self.reset_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",command = self.time_reset)
        btn_back=Button(self.back_frame,image=self.back_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",command=lambda:self.controller.show_frame("mainmenu"))
        self.btn_hour_up=Button(self.upset_frame,image=self.up_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=93,command=self.hour_up)
        self.btn_min_up=Button(self.upset_frame,image=self.up_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=93,command=self.minute_up)
        self.btn_sec_up=Button(self.upset_frame,image=self.up_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=93,command=self.second_up)
        self.btn_hour_down=Button(self.downset_frame,image=self.down_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=95,command=self.hour_down)
        self.btn_min_down=Button(self.downset_frame,image=self.down_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=95,command=self.minute_down)
        self.btn_sec_down=Button(self.downset_frame,image=self.down_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9",width=95,command=self.second_down)
        self.label_time=Label(self.clock_frame,text="00:00:00",font=("Helvetica",60),fg="#2c3e50",bg="#bdc3c7",activebackground="#dfe6e9")
        #self.btn_speech=Button(self.top_frame,image=self.speech_img,bg="#bdc3c7",relief="flat",activebackground="#dfe6e9")
        #스피치 버튼 명령어 넣기
        

        #self.btn_speech.grid(row=0,column=0,padx=10)
        self.label_time.grid(row=0,padx=3)
        self.btn_hour_up.grid(row=0,column=0)
        self.btn_min_up.grid(row=0,column=1,padx=9)
        self.btn_sec_up.grid(row=0,column=2)
        self.btn_hour_down.grid(row=0,column=0)
        self.btn_min_down.grid(row=0,column=1,padx=9)
        self.btn_sec_down.grid(row=0,column=2)
        self.btn_control.grid(row=0,column=0,padx=70)
        self.btn_reset.grid(row=0,column=1)
        btn_back.grid(row=0,column=0)
    """
    def speech_time_set(self,h,m,s):
        self.hour = h
        self.minute = m
        self.second = s
        new_time = "{:02}:{:02}:{:02}".format(self.hour,self.minute,self.second)
        self.label_time.config(text=new_time)
        self.second_total()
    """
    def hour_up(self):
        self.hour += 1
        if self.hour > 23:
            self.hour = 0
        self.time_set()
    def minute_up(self):
        self.minute += 1
        if self.minute > 59:
            self.minute = 0
        self.time_set()
    def second_up(self):
        self.second += 1
        if self.second > 59:
            self.second = 0
        self.time_set()
    
    def hour_down(self):
        self.hour -= 1
        if self.hour < 0:
            self.hour = 23
        self.time_set()
    def minute_down(self):
        self.minute -= 1
        if self.minute < 0:
            self.minute = 59
        self.time_set()
    def second_down(self):
        self.second -= 1
        if self.second < 0:
            self.second = 59
        self.time_set()
    
    def time_set(self):
        self.hours = str(self.hour)
        self.minutes = str(self.minute)
        self.seconds = str(self.second)
        if self.hour < 10:
            self.hours = "0" + str(self.hour)
        else:
            self.hours = str(self.hour)
        if self.minute < 10:
            self.minutes = "0" + str(self.minute)
        else:
            self.minutes = str(self.minute)
        if self.second < 10:
            self.seconds = "0" + str(self.second)
        else:
            self.seconds = str(self.second)
        new_time_label = self.hours + ":" + self.minutes + ":" + self.seconds     
        self.label_time.config(text=new_time_label)
        self.second_total()
    
    def second_total(self):
        self.total_second = self.hour*3600 + self.minute*60 + self.second
    
    def timer_loop(self,total):
        hour_left, second_left = divmod(total,3600)
        minute_left, second_left = divmod(second_left,60)
        

        if total != 0 :
            if self.mode == "RUNNING":
                total -= 1
                new_time = "{:02}:{:02}:{:02}".format(hour_left, minute_left, second_left)
                self.label_time.config(text=new_time)   
            elif self.mode == "STOP":
                return
            self.label_time.after(1000,self.timer_loop,total)
        elif total == 0 :
            sound = mixer.Sound(r"music/ding.wav")
            mixer.Sound.play(sound)
            self.time_reset()           

    
    
    def change_control(self):
        if self.mode == "STOP":
            self.mode = "RUNNING"
            print(self.mode)
            self.timer_loop(self.total_second)
        elif self.mode == "RUNNING":
            self.mode = "PAUSE"
            print(self.mode)
        elif self.mode == "PAUSE":
            self.mode = "RUNNING"
            print(self.mode)
        self.change_button()
    
    def change_button(self):
        if self.mode == "STOP":
            self.btn_hour_up.config(state=NORMAL)
            self.btn_min_up.config(state=NORMAL)
            self.btn_sec_up.config(state=NORMAL)
            self.btn_hour_down.config(state=NORMAL)
            self.btn_min_down.config(state=NORMAL)
            self.btn_sec_down.config(state=NORMAL)
            self.btn_control.config(image=self.start_img)
        elif self.mode == "RUNNING":
            self.btn_hour_up.config(state=DISABLED)
            self.btn_min_up.config(state=DISABLED)
            self.btn_sec_up.config(state=DISABLED)
            self.btn_hour_down.config(state=DISABLED)
            self.btn_min_down.config(state=DISABLED)
            self.btn_sec_down.config(state=DISABLED)
            self.btn_control.config(image=self.pause_img)
        elif self.mode == "PAUSE":
            self.btn_hour_up.config(state=DISABLED)
            self.btn_min_up.config(state=DISABLED)
            self.btn_sec_up.config(state=DISABLED)
            self.btn_hour_down.config(state=DISABLED)
            self.btn_min_down.config(state=DISABLED)
            self.btn_sec_down.config(state=DISABLED)
            self.btn_control.config(image=self.resume_img)
        
    def time_reset(self):
        self.mode = "STOP"
        self.label_time.config(text="00:00:00")
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.change_button()
    """
    def listen_print_loop(self,responses):
        
        Iterates through server responses and prints them.

        The responses passed is a generator that will block until a response
        is provided by the server.

        Each response may contain multiple results, and each result may contain
        multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.

        In this case, responses are provided for interim results as well. If the
        response is an interim one, print a line feed at the end of it, to allow
        the next result to overwrite it, until the response is a final one. For the
        final one, print a newline to preserve the finalized transcription.
        
        timer = self.sp_timer
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                timer
                if len(timer) > 0:
                    timer.clear()
                
                index = 0
                idx_hour = 0
                idx_min = 0
                idx_sec = 0
                time_hour = ""
                time_min = ""
                time_sec = ""
                t_hour = self.sp_hour 
                t_min  = self.sp_min
                t_sec  = self.sp_sec
                
                timer = transcript.split()
                for i in timer:               
                    if "시간" in timer[index]:
                        idx_hour = index
                        timer[idx_hour] = " " + timer[idx_hour]
                        time_hour = timer[idx_hour][len(timer[idx_hour])-4:len(timer[idx_hour])-2]
                        if " " in time_hour:
                            time_hour = time_hour.replace(" ","")
                        
                    if '분' in timer[index]:
                        idx_min = index
                        timer[idx_min] = " " + timer[idx_min]
                        time_min = timer[idx_min][len(timer[idx_min])-3:len(timer[idx_min])-1]
                        if " " in time_min:
                            time_min = time_min.replace(" ","")
                            
                    if '초' in timer[index]:
                        idx_sec = index
                        timer[idx_sec] = " " + timer[idx_sec]
                        time_sec = timer[idx_sec][len(timer[idx_sec])-3:len(timer[idx_sec])-1]
                        if " " in time_sec:
                            time_sec = time_sec.replace(" ","")
                    index += 1
                if len(time_hour) > 0:
                    t_hour = int(time_hour)
                else:
                    t_hour = 0
                    print(type(t_hour))
                
                if len(time_min) > 0:
                    t_min = int(time_min)
                else:
                    t_min = 0
                    print(type(t_min))
                
                if len(time_sec) > 0:
                    t_sec = int(time_sec)
                else:
                    t_sec = 0
                    print(type(t_sec))
                self.speech_time_set(t_hour,t_min,t_sec)
                break
    def main(self):
        # See http://g.co/cloud/speech/docs/languages
        # for a list of supported languages.
        language_code = 'ko-KR'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            self.listen_print_loop(responses)  
    """