from tkinter import *
import tkinter.font as font
from tkinter import ttk
import threading
import testRecord
import testPlay
import exporter
import deleter

class GUIWindow:

    def __init__(self):
        self.record_thread=threading.Thread()
        self.play_thread=threading.Thread()
        self.has_audio=False
        self.is_playing=False
        self.is_recording=False
        self.bd="16"
        self.df="1"

    def playRecAudio(self, button):

        depth=self.bd
        dfactor=self.df

        if self.is_recording:
            self.is_recording=False
            print(self.is_recording)
            button["text"]="PLAY"
            self.record_thread.join()
            self.record_thread=None
            self.has_audio=True
        elif not self.has_audio:  #RECORDING PASS IN VALUES HERE AT ARGS
            self.is_recording=True
            button["text"]="RECORDING"
            self.record_thread = threading.Thread(target=testRecord.recordAudio, args=(self,depth,dfactor,))
            self.record_thread.start()
        elif self.is_playing:
            button["text"]="PLAY"
            self.is_playing=False
        else:
            button["text"]="PAUSE"
            self.is_playing=True
            self.play_thread = threading.Thread(target=testPlay.playAudio)
            self.play_thread.start()


    def makeGuiWindow(self):

        def stopAudio():
            pass
            #call stopAudio

        def reverseAudio():
            pass

        def restartAudio():
            pass

        def deleteAudio():
            self.has_audio = False
            deleter.delete()
            pass

        def exportAudio():
            exporter.export()
            pass

        def adjustVol():
            pass

        def adjustPit():
            pass


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

        reverseAudioButton = Button(text="REVERSE",command=reverseAudio()).place(relx=.57, rely=.6, relwidth=.07, relheight=.05)
        resetAudioButton = Button(text="RESTART", command=restartAudio()).place(relx=.36, rely=.6, relwidth=.07, relheight=.05)
        deleteAudioButton = Button(text="Delete\nRecording", command= lambda : deleteAudio()).place(relx=.04, rely=.04, relwidth=.08, relheight=.08)
        exportAudioButton = Button(text="Export Audio", command= lambda : exportAudio()).place(relx=.76, rely=.85, relwidth=.17, relheight=.07)
        audioProgressBar = ttk.Progressbar(mode="determinate", orient="horizontal").place(relx=.2, rely=.52, relheight=.05, relwidth=.6)
        volumeSlider = Scale(from_=0, to=160, showvalue=0, orient=HORIZONTAL, tickinterval=0, command=adjustVol()).place(relx=.05, rely=.72, relheight=.08, relwidth=.27)
        pitchSlider = Scale(from_=0, to=160, showvalue=0, orient=HORIZONTAL, tickinterval=0, command=adjustPit()).place(relx=.05, rely=.89, relheight=.08, relwidth=.27)
        myFont = font.Font(family="Helvetica", size=16, weight='bold', slant='italic')
        volumeLabel = Label(text="Volume", font=myFont).place(relx=.04, rely=.65)
        pitchLabel = Label(text="Pitch", font=myFont).place(relx=.04, rely=.82)
        sampleRates = ["44.1k", "22.05k","11.025k", "5.5125k", "2.75625k"]
        bitDepths = ["16","8"]
        sampleRateInitial = StringVar()
        sampleRateInitial.set("44.1k")
        sampleRateMenu = OptionMenu(window,sampleRateInitial,*sampleRates, command=self.selectSample).place(relx=.15, rely=.04, relwidth=.2, relheight=.1)
        bitDepthInitial = StringVar()
        bitDepthInitial.set("16")
        bitDepthMenu = OptionMenu(window,bitDepthInitial,*bitDepths, command=self.selectDepth).place(relx=.36, rely=.04, relwidth=.2, relheight=.1)
        
        
        window.mainloop()

    def selectSample(self,selection):
        if selection == "44.1k":
            self.df="1"
        elif selection == "22.05k":
            self.df="2"
        elif selection == "11.025k":
            self.df="4"
        elif selection == "5.5125k":
            self.df="8"
        elif selection == "2.75625k":
            self.df="16"
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