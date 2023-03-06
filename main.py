from sys import executable
from os import path, abort
from threading import Thread
from time import sleep as wait
from tkinter import Tk, IntVar, Frame, Entry, Label, messagebox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from pygame import mixer

    





class Timer: #Object for handling counting down and time.

    def __init__(self): #Initializes timer class, loads the alert in exe's directory.
        self.timer_paused = False
        self.counting_down = False
        mixer.init()
        mixer.music.load("%s\\alert.mp3"%dir)
    
    def start(self): #Creates a thread that handles counting the timer down.
        self.time_left = window.hour.get() * 3600 + window.min.get() * 60 + window.sec.get()
        self.counter = Thread(target= lambda: self.count_down())
        self.counting_down = True
        self.counter.start()


    def stop(self): #Stops timer and also joins countdown thread.
        mixer.music.stop()
        self.timer_paused = False
        self.counting_down = False
        self.counter.join()
    
    
    def count_down(self): #Counts down timer until 0 is reached, then calls function.
        for i in range(self.time_left, 0, -1):
            if not self.counting_down:
                break
            while self.timer_paused:
                pass
            wait(1)
        else:
            self.time_out()

        
    def pause(self): #Inverts bool variable when called.
        self.timer_paused = not self.timer_paused 

    def time_out(self): #Plays selected alert file.
        mixer.music.play(100)

class Window: #Object that handles the initialization of the "Set Time" window.

    def __init__(self): #Initializes time-setting window.
        master.protocol("WM_DELETE_WINDOW", (lambda: self.check_vars()))

        self.vcmd = (master.register(self.callback), '%P', '%W')
        self.hour = IntVar(value = 0)
        self.min = IntVar(value = 0)
        self.sec = IntVar(value = 10)

        self.hour_entry = self.make_entry("gray", 5, 10, self.hour, 4, 'hour')
        self.min_entry = self.make_entry("gray", 5, 35, self.min, 4, 'min')
        self.sec_entry = self.make_entry("gray", 5, 60, self.sec, 4, 'sec')

    def make_entry(self, frame_color, x, y, var, width, text): # Quick and easy way to make an entry inside the time-setting window.
        frame = Frame(master, bg=frame_color, bd=0); frame.place(x=x, y=y)
        input = Entry(frame, validate= 'key', validatecommand=self.vcmd, textvariable=var, width=width, relief='solid', borderwidth=0); input.pack(padx=1, pady=1)
        text = Label(master, text=text, ); text.place(x=x+30, y=y-1)
        return {"FRAME": frame, "INPUT": input, "TEXT": text}
    
    def callback(self, text, wid): #Checks if a time variable is an integer, is less than 4 digits long, or null.
        if str.isdecimal(text) or not text:
            if len(str(text)) >= 5:
                return False
            text = text if text else 0
            return True
        return False

    def check_vars(self): #Sets variables to 0 if they are null.
        try :self.hour.get()
        except: self.hour.set(0)

        try :self.min.get()
        except: self.min.set(0)

        try :self.sec.get()
        except: self.sec.set(0)
        master.withdraw()

        

class TaskBarIcon: #Object that handles the task bar icon and its functionality.

    def __init__(self): #Initializes task bar and its respective options.

        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        systray = QSystemTrayIcon()
        systray.setIcon(QIcon("%s\\icon.ico"%path.dirname(path.abspath(__file__))))
        systray.setToolTip("Onready Timer")

        systray.setVisible(True)

        self.menu = QMenu()
        self.entries = ["Set Time", "Start", "Quit"]
        self.commands = [lambda: master.deiconify(), lambda: self.start(), lambda: abort()]
        self.actions = {}


        for entry in self.entries: #Runs through and enters the entries into the systray.
            action = QAction(entry)
            self.menu.addAction(action)
            action.triggered.connect(self.commands[self.entries.index(entry)])
            self.actions[entry] = action

        systray.setContextMenu(self.menu)
        
        master.mainloop()
        app.exec_()
    
    def start(self): #Function that is called when the "Start" button is pressed. Swaps "Start" button to "Pause" and creates "Stop" button. 
        self.actions["Set Time"].setDisabled(True)
        self.actions["Start"].setText("Pause")
        self.actions["Start"].triggered.disconnect()
        self.actions["Start"].triggered.connect(lambda: self.pause())

        action = QAction("Stop")
        self.actions["Stop"] = action
        self.menu.insertAction(self.actions["Quit"], action)
        self.actions["Stop"].triggered.connect(lambda: self.stop())
        timer.start()
        

    def stop(self): #Function that is called when the "Stop" button is pressed. Swaps "Pause" button back to "Start" and deletes "Stop" button. 
        self.actions["Set Time"].setDisabled(False)
        self.actions["Start"].setText("Start")
        self.actions["Start"].triggered.disconnect()
        self.actions["Start"].triggered.connect(lambda: self.start())

        self.menu.removeAction(self.actions["Stop"])
        self.actions["Stop"] = None
        self.actions["Start"].setText("Start")
        timer.stop()

    def pause(self): #Function that is called when the "Pause" button is pressed. Swaps button between "Pause" and "Unpause" based on Timer's state.
        if not timer.timer_paused:
            self.actions["Start"].setText("Unpause")
        else:
            self.actions["Start"].setText("Pause")
        timer.pause()
        

    
    


        


        


master = Tk() #Master window
master.resizable(False, False)
master.attributes('-toolwindow', True)
master.geometry('100x100')
master.attributes('-topmost', 'true')
master.title('Set Time')
master.withdraw()

if str(path.abspath(path.dirname(executable))).split("\\")[-1].__contains__("Python"): #Checks to see if the program is running from VSC or is compiled.
    dir = path.dirname(path.abspath(__file__)) #VSC
else:
    dir = path.abspath(path.dirname(executable)) #EXE

if path.exists("%s\\alert.mp3"%dir):
    pass
else:
    messagebox.showerror("Onready Timer", "'alert.mp3' not found. Please place an MP3 file of your choice into the executable's directory rename it to 'alert', then re-run the program.")
    abort()

timer = Timer()
window = Window()
systray = TaskBarIcon()







