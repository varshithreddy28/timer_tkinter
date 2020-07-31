import tkinter as tk
from tkinter import ttk
import datetime
import threading
import winsound

try:
    from ctypes import windll
    windll.shcore.SetProcessDpAwareness(1)
except:
    pass

#colours:
COLOURP="#1E90FF" #blue
COLOURSE="#104E8B" #black
COLOURT="#6495ED" #white
COLOURF ="#4B0082" #violet
COLOURSIX="#080808" #lightblue
COLOURB="#308014" #green


class Timer(tk.Tk):
    def __init__(self):
        super().__init__()

        #STYLING
        style=ttk.Style(self)
        style.theme_use('clam')
        style.configure("Time.Tframe",background=COLOURT)
        style.configure("BackGroung.TFrame",background=COLOURP)
        style.configure(
            "TimerText.TLabel",
            background=COLOURT,
            foreground=COLOURSIX,
            font="Courier 45"
        )

        style.configure(
            "LightText.TLabel",
            background=COLOURP,
            foreground=COLOURF
        )

        style.configure(
            "TimeButton.TButton",
            background=COLOURB,
            foreground=COLOURF,
        )

        style.map(  #mouse cursor is present or not
            "TimerButton.TButton",
            background=[("active",COLOURSE),("disabled",COLOURSIX)]
        )

        self["background"]=COLOURP

        self.title('Timer')
        self.frame=dict()
        self.time=tk.StringVar()
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        #declaration in global
        self.original=tk.StringVar(value=25)
        self.second=tk.StringVar(value=00)
        self.popup=tk.StringVar(value='Timer is on')
        
        container=ttk.Frame(self)
        container.grid(sticky='NSEW')

        

        ftimer=Time(container,self)
        ftimer.grid(row=0,column=0,sticky='NSEW')
        fsetting=Setting(container,self)
        fsetting.grid(row=0,column=0,sticky='NSEW')
        ftimer.tkraise()
        self.frame[Time]=ftimer
        self.frame[Setting]=fsetting
    def selectframe(self,container):
        frames=self.frame[container]
        frames.tkraise()

class Time(ttk.Frame):
    def __init__(self,container,controller):
        super().__init__(container)
        #means it brings all the timer values from the above class
        
        self.timerrunning=False
        self._stoptimer=None#_ means it can be only used in the class
        self["style"]="BackGroung.TFrame"

        self.controller=controller
        original=int(controller.original.get())
        second=int(controller.second.get())
        self.time=tk.StringVar(value=f'{original:02d}:{second:02d}')
        tdisp=ttk.Frame(self, height="100", style="Timer.TFrame")
        tdisp.grid(row=1, column=0, columnspan=2, padx=10,pady=10, sticky="NSEW")
        self.ltime=ttk.Label(tdisp,textvariable=self.time,style="TimerText.TLabel")
        self.ltime.place(relx=0.5, rely=0.5, anchor="center")

        eframe=ttk.Frame(self ,padding=10, style="Background.TFrame")
        eframe.grid(row=2,column=0,columnspan=2,sticky='EW')
        eframe.columnconfigure((0,1,2),weight=1)
        self.sbutton=ttk.Button(eframe,text='Start',cursor='hand2',
        style="TimeButton.TButton",command=self.start)
        self.sbutton.grid(row=2,column=0,sticky='EW',padx=5,pady=5)

        self.stbutton=ttk.Button(eframe,text='Pause',cursor='hand2',
        style="TimeButton.TButton",
        command=self.stop)
        self.stbutton.grid(row=2,column=1,sticky='EW',padx=5,pady=5)

        self.stbutton["state"]="disabled"
        self.reset=ttk.Button(eframe,text='Reset',cursor='hand2',
        style="TimeButton.TButton"
        ,command=self.reset)
        self.reset.grid(row=2,column=2,sticky='EW',padx=5,pady=5)

        self.obutton=ttk.Button(self,text='Settings',
        style="TimerButton.TButton",
        cursor='hand2',
        command=lambda :controller.selectframe(Setting))
        self.obutton.grid(row=0,column=1,sticky='E',padx=5,pady=1)

    def start(self):
        self.timerrunning=True
        self.starts()
        self.sbutton["state"]="disabled"
        self.stbutton["state"]="enabled"
    def stop(self):
        self.timerrunning=False
        self.starts()
        self.sbutton["state"]="enabled"
        self.stbutton["state"]="disabled"
    def reset(self):
        self.stop()
        original=int(self.controller.original.get())
        second=int(self.controller.second.get())
        self.time.set(f'{original:02d}:{second:02d}')
        
    def starts(self):
        timer=self.time.get()
        minutes,seconds=timer.split(':')
        if self.timerrunning and timer !='00:00' :
            minutes,seconds=timer.split(':')
            if int(seconds)>0:
                seconds=int(seconds)-1
                minutes=int(minutes)
            elif int(minutes)>0:
                seconds=59
                minutes=int(minutes)-1
            self.time.set(f'{int(minutes):02d}:{int(seconds):02d}')
            
            threading.Timer(1.0,self.starts).start()
        elif int(minutes)==00 and int(seconds)==00:
            dur=10000 #millysec
            freq=400 #hz
            winsound.Beep(freq,dur)
        

class Setting(ttk.Frame):
    def __init__(self,container,controller):
        super().__init__(container)

        self["style"]="BackGroung.TFrame"

        self.controller=controller
        pop=controller.popup.get()
        
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        #controller.original.set('00:15')
        settings=ttk.Frame(self,
            padding="30 15 30 15",
            style="Background.TFrame")
        settings.grid(row=0,column=0,sticky='EW',padx=10,pady=10)
        
        settings.columnconfigure(0, weight=1)
        settings.rowconfigure(1, weight=1)

        label1=ttk.Label(settings,text='Minutes')
        label1.grid(row=1,column=0)
        
        spin1=tk.Spinbox(settings,from_=00,to=59,
        textvariable=controller.original,
        increment=1,
        width=10,
        justify='center'
        )
        spin1.grid(row=1,column=1,sticky='EW',padx=5,pady=5)

        label2=ttk.Label(settings,text='Seconds')
        label2.grid(row=2,column=0)

        spin2=tk.Spinbox(settings,from_=00,to=59,text='Seconds',
        textvariable=controller.second,
        increment=1,
        width=10,
        justify='center'
        )
        spin2.grid(row=2,column=1,sticky='EW',padx=5,pady=5)

        button=ttk.Button(settings,text='Back',cursor='hand2',style="TimerButton.TButton",command=lambda :controller.selectframe(Time))
        button.grid(row=4,column=0,sticky='EW',padx=5,pady=1)
root=Timer()

root.mainloop()