from tkinter import *
import tkinter.font as font
from tkinter import ttk
import time

def playRecAudio():
    pass

def stopAudio():
    pass
    #call stopAudio

def reverseAudio():
    pass

def restartAudio():
    pass

def deleteAudio():
    pass

def exportAudio():
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

playAudioButton = Button(text="RECORD",command=playRecAudio()).place(relx=.44, rely=.6, relwidth=.12, relheight=.07)
reverseAudioButton = Button(text="REVERSE",command=reverseAudio()).place(relx=.57, rely=.6, relwidth=.07, relheight=.05)
resetAudioButton = Button(text="RESTART", command=restartAudio()).place(relx=.36, rely=.6, relwidth=.07, relheight=.05)
deleteAudioButton = Button(text="Delete\nRecording", command=deleteAudio()).place(relx=.04, rely=.04, relwidth=.08, relheight=.08)
exportAudioButton = Button(text="Export Audio", command=exportAudio()).place(relx=.76, rely=.85, relwidth=.17, relheight=.07)
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
sampleRateMenu = OptionMenu(window,sampleRateInitial,*sampleRates).place(relx=.15, rely=.04, relwidth=.2, relheight=.1)
bitDepthInitial = StringVar()
bitDepthInitial.set("16")
bitDepthMenu = OptionMenu(window,bitDepthInitial,*bitDepths).place(relx=.36, rely=.04, relwidth=.2, relheight=.1)


window.mainloop()

