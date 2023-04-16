from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from pydub import AudioSegment
import threading
from recorder import recorder
from looper import looper
from processor import processor
from exporter import exporter
import deleter
import time

class GUIWindow:

    def __init__(self):
        self.record_thread=threading.Thread()
        self.play_thread=threading.Thread()
        self.has_audio=False
        self.is_playing=False
        self.is_recording=False
        self.bd="16"
        self.df="1"
        self.rec44k = recorder(44100)
        self.rec48k = recorder(48000)
        self.looper = looper()
        self.exp = exporter()
        self.proc = None
        self.audio_seg = None
        self.is_44k = True

    def playRecAudio(self, button): #needs to be changed to reflect processing

        depth=self.bd
        dfactor=self.df

        if self.is_recording:
            self.is_recording=False
            print(self.is_recording)
            button["text"]="PLAY"
            self.record_thread.join()
            self.record_thread=None
            self.has_audio=True
            if(self.is_44k):
                self.proc = processor(44100, "decimated.wav")
            else:
                self.proc = processor(48000, "decimated.wav")
            self.audio_seg = self.proc.get_audiosegment()
            print(self.audio_seg)
        elif not self.has_audio:  
            self.is_recording=True
            button["text"]="RECORDING"
            if self.is_44k:
                self.record_thread = threading.Thread(target=self.rec44k.record, args=(self,depth,dfactor,))
            else:
                self.record_thread = threading.Thread(target=self.rec48k.record, args=(self,depth,dfactor,))
            self.record_thread.start()
        elif self.is_playing:
            button["text"]="PLAY"
            self.is_playing=False
            self.play_thread.join()
            self.play_thread=None
        else:
            print("RUNNING THE THING")
            self.exp.export2(self.audio_seg)
            button["text"]="PAUSE"
            self.is_playing=True
            self.play_thread = threading.Thread(target=self.looper.loop_audio, args=("modified.wav",self,))
            self.play_thread.start()


    def makeGuiWindow(self):

        def reverseAudio(): #test
            self.proc.reverse(self.audio_seg)

        def restartAudio(): #reset audio back to previous state
            pass

        def deleteAudio(): #reset processor
            self.has_audio = False
            self.proc = None
            self.audio_seg = None
            deleter.delete()
            pass

        def exportAudio(): #add additional formats?
            self.exp.export(self.audio_seg)
            pass

        def adjustVol(self):
            #self.audio_seg = self.proc.amplify(audio_seg, 6)
            pass

        def adjustPit(self,pitch_mult): #speed controller
            #self.audio_seg = alter_speed(self.audio_seg,pitch_mult)
            pass

        def adjustTrim(self,startpoint,endpoint): 
            #trim(self.audio_seg,startpoint,endpoint)
            pass

        def on_close():#closes threads on shutdown, also confirms user wants to quit
            if messagebox.askokcancel("Quit", "You will lose all unexported files, do you still want to quit?"):
                if(self.is_recording):
                    self.is_recording=False
                    self.record_thread.join()
                    self.record_thread=None
                elif(self.is_playing): 
                    self.is_playing=False
                    self.play_thread.join()
                    self.play_thread=None
                window.destroy()


        audioLength = None
        def audioProgress():
            audioProgress['value']+=.05/audioLength
            if(not audioProgress['value']>=100):
                window.after(50, audioProgress)

        window=Tk()
        window.title('Compugene')
        window.geometry("600x400+40+50")
        #myCanvas = Canvas(window)
        #myCanvas.place(x=-2, y=-2, relwidth=1.02, relheight=1.02)

        #screenHeight = myCanvas.winfo_height()
        #screenWidth = myCanvas.winfo_width()
        #recordButton = myCanvas.create_oval(screenWidth*.45, screenHeight*.45, screenWidth*.55, screenHeight*.45 + (screenWidth*.1))
        #tri1points = [screenWidth+50,screenHeight,screenWidth+50,screenHeight+30,screenWidth,screenHeight]
        #myCanvas.create_polygon(tri1points, outline=None, fill='#ef2497')

        scrHeight = window.winfo_height()
        scrWidth = window.winfo_width()

        playRecAudioButton = ttk.Button(text="RECORD")
        playRecAudioButton.place(relx=.44, rely=.6, relwidth=.12, relheight=.07)
        playRecAudioButton.configure(command= lambda : self.playRecAudio(playRecAudioButton))

        reverseAudioButton = Button(text="REVERSE",command= lambda : reverseAudio(self)).place(relx=.57, rely=.6, relwidth=.07, relheight=.05)
        resetAudioButton = Button(text="RESTART", command=lambda : restartAudio()).place(relx=.36, rely=.6, relwidth=.07, relheight=.05)
        deleteAudioButton = Button(text="Delete\nRecording", command= lambda : deleteAudio()).place(relx=.04, rely=.04, relwidth=.08, relheight=.08)
        exportAudioButton = Button(text="Export Audio", command= lambda : exportAudio()).place(relx=.76, rely=.85, relwidth=.17, relheight=.07)
        audioProgressBar = ttk.Progressbar(mode="determinate", orient="horizontal").place(relx=.2, rely=.52, relheight=.05, relwidth=.6)
        volumeSlider = Scale(from_=0, to=160, showvalue=0, orient=HORIZONTAL, tickinterval=0, command=lambda : adjustVol(self)).place(relx=.05, rely=.72, relheight=.08, relwidth=.27)
        pitchSlider = Scale(from_=0, to=160, showvalue=0, orient=HORIZONTAL, tickinterval=0, command=lambda : adjustPit(self,0)).place(relx=.05, rely=.89, relheight=.08, relwidth=.27)
        myFont = font.Font(family="Helvetica", size=16, weight='bold', slant='italic')
        volumeLabel = Label(text="Volume", font=myFont).place(relx=.04, rely=.65)
        pitchLabel = Label(text="Pitch", font=myFont).place(relx=.04, rely=.82)
        sampleRates = ["44.1k", "22.05k","11.025k", "5.5125k", "2.75625k","48k","24k","12k","6k","3k"]
        bitDepths = ["16","8"]
        sampleRateInitial = StringVar()
        sampleRateInitial.set("44.1k")
        sampleRateMenu = OptionMenu(window,sampleRateInitial,*sampleRates, command=self.selectSample).place(relx=.15, rely=.04, relwidth=.2, relheight=.1)
        bitDepthInitial = StringVar()
        bitDepthInitial.set("16")
        bitDepthMenu = OptionMenu(window,bitDepthInitial,*bitDepths, command=self.selectDepth).place(relx=.36, rely=.04, relwidth=.2, relheight=.1)
        
        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()

    def selectSample(self,selection):
        if selection == "44.1k":
            self.df="1"
            self.is_44k = True
        elif selection == "22.05k":
            self.df="2"
            self.is_44k = True
        elif selection == "11.025k":
            self.df="4"
            self.is_44k = True
        elif selection == "5.5125k":
            self.df="8"
            self.is_44k = True
        elif selection == "2.75625k":
            self.df="16"
            self.is_44k = True
        elif selection == "48k":
            self.df="1"
            self.is_44k = False
        elif selection == "24k":
            self.df="2"
            self.is_44k = False
        elif selection == "12k":
            self.df="4"
            self.is_44k = False
        elif selection == "6k":
            self.df="8"
            self.is_44k = False
        elif selection == "3k":
            self.df="16"
            self.is_44k = False
        else:  
            print("Not valid sample rate")

    def selectDepth(self,selection):
        if selection == "16":
            self.bd="16"
        elif selection == "8":
            self.bd="8"
        else:  
            print("Not valid sample rate")

    def getAudio(self):
        return self.has_audio

    def getPlaying(self):
        return self.is_playing

    def getRecording(self):
        return self.is_recording


if __name__ == '__main__':
    myGui = GUIWindow()
    myGui.makeGuiWindow()