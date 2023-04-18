from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from pydub import AudioSegment
import threading
from recorder import recorder
from looper import looper
from processor import processor
from exporter import exporter
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
        self.rec44k = recorder(44100)
        self.rec48k = recorder(48000)
        self.looper = looper()
        self.exp = exporter()
        self.vol= None
        self.pitch = None
        self.revflag = False
        self.proc = None
        self.audio_seg = None
        self.is_44k = True
        self.playRecAudioImage = None
        self.playRecAudioButton = None
        self.reverseAudioImage = None
        self.reverseAudioButton = None
        self.processAudioImage = None
        self.processAudioButton = None
        self.deleteAudioImage = None
        self.deleteAudioButton = None
        self.exportAudioButton = None
        self.exportAudioImage = None

    def playRecAudio(self, button): 

        depth=self.bd
        dfactor=self.df

        if self.is_recording:
            self.is_recording=False
            print(self.is_recording)
            self.playRecAudioImage = PhotoImage(file =".\\png\\Play_NotPress.png")
            button.configure(image=self.playRecAudioImage)
            self.record_thread.join()
            self.record_thread=None
            self.has_audio=True
            if(self.is_44k):
                self.proc = processor(44100, "decimated.wav")
            else:
                self.proc = processor(48000, "decimated.wav")
            self.audio_seg = self.proc.get_audiosegment()
        elif not self.has_audio:  
            self.is_recording=True
            if self.is_44k:
                self.record_thread = threading.Thread(target=self.rec44k.record, args=(self,depth,dfactor,))
            else:
                self.record_thread = threading.Thread(target=self.rec48k.record, args=(self,depth,dfactor,))
            self.record_thread.start()
            
        elif self.is_playing:
            self.playRecAudioImage = PhotoImage(file =".\\png\\Play_NotPress.png")
            button.configure(image=self.playRecAudioImage)
            self.is_playing=False
            self.play_thread.join()
            self.play_thread=None
        else:
            print("RUNNING THE THING")
            self.exp.export2(self.audio_seg)
            self.playRecAudioImage = PhotoImage(file =".\\png\\Stop_NotPress.png")
            button.configure(image=self.playRecAudioImage)
            self.is_playing=True
            self.play_thread = threading.Thread(target=self.looper.loop_audio, args=("modified.wav",self,))
            self.play_thread.start()

    def changePlayRecAudioLook(self, event):
            if self.is_recording:
                self.playRecAudioImage = PhotoImage(file =".\\png\\Stop_Press.png")
                self.playRecAudioButton.configure(image=self.playRecAudioImage)
            elif not self.has_audio:
                self.playRecAudioImage = PhotoImage(file =".\\png\\Record_Press.png")
                self.playRecAudioButton.configure(image=self.playRecAudioImage)
            elif self.is_playing:
                self.playRecAudioImage = PhotoImage(file =".\\png\\Stop_Press.png")
                self.playRecAudioButton.configure(image=self.playRecAudioImage)
            else:
                self.playRecAudioImage = PhotoImage(file =".\\png\\Play_Press.png")
                self.playRecAudioButton.configure(image=self.playRecAudioImage)
    
    def changeReverseAudioLook(self, event):
        self.reverseAudioImage = PhotoImage(file =".\\png\\Reverse_Press.png")
        self.reverseAudioButton.configure(image=self.reverseAudioImage)

    def changeProcessAudioLook(self, event):
        self.processAudioImage = PhotoImage(file =".\\png\\Process_Audio_Press.png")
        self.processAudioButton.configure(image=self.processAudioImage)

    def changeDeleteAudioLook(self, event):
        self.deleteAudioImage = PhotoImage(file =".\\png\\Delete_Recording_Press.png")
        self.deleteAudioButton.configure(image=self.deleteAudioImage)

    def changeExportAudioLook(self, event):
        self.exportAudioImage = PhotoImage(file =".\\png\\Export_Press.png")
        self.exportAudioButton.configure(image=self.exportAudioImage)

    def makeGuiWindow(self):

        def processAudio(): 
            self.processAudioImage = PhotoImage(file =".\\png\\Process_Audio_NotPress.png")
            self.processAudioButton.configure(image=self.processAudioImage)
            self.audio_seg=self.proc.get_master() #revert audio_seg back to its previous state
            adjustVol()
            adjustPit()
            if self.revflag:
                reverseAudio()
            #adjustTrim(startpoint,endpoint)

        def deleteAudio(button):
            button["text"]="RECORD"
            self.has_audio = False
            self.proc = None
            self.audio_seg = None
            self.revflag = False
            deleter.delete()
            self.playRecAudioImage = PhotoImage(file =".\\png\\Record_NotPress.png")
            self.playRecAudioButton.configure(image=self.playRecAudioImage)
            self.deleteAudioImage = PhotoImage(file =".\\png\\Delete_Recording_NotPress.png")
            self.deleteAudioButton.configure(image=self.deleteAudioImage)

        def exportAudio(): #add additional formats?
            self.exp.export(self.audio_seg)
            self.exportAudioImage = PhotoImage(file =".\\png\\Export_NotPress.png")
            self.exportAudioButton.configure(image=self.exportAudioImage)
            pass

        def adjustVol():
            self.audio_seg = self.proc.amplify(self.audio_seg, self.vol.get())

        def adjustPit(): #speed controller
            self.audio_seg = self.proc.alter_speed(self.audio_seg, self.pitch.get())

        def reverseAudio(): 
            self.audio_seg = self.proc.reverse(self.audio_seg)

        def adjustTrim(self,startpoint,endpoint): 
            #trim(self.audio_seg,startpoint,endpoint)
            pass

        def setReverse():
            self.revflag = not self.revflag
            self.reverseAudioImage=PhotoImage(file =".\\png\\Reverse_NotPress.png")
            self.reverseAudioButton.configure(image=self.reverseAudioImage)

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
        window.minsize(1200,700)
        window.config(bg='white')

        self.vol=IntVar()
        self.pitch=DoubleVar()
        #myCanvas = Canvas(window)
        #myCanvas.place(x=-2, y=-2, relwidth=1.02, relheight=1.02)

        #screenHeight = myCanvas.winfo_height()
        #screenWidth = myCanvas.winfo_width()
        #recordButton = myCanvas.create_oval(screenWidth*.45, screenHeight*.45, screenWidth*.55, screenHeight*.45 + (screenWidth*.1))
        #tri1points = [screenWidth+50,screenHeight,screenWidth+50,screenHeight+30,screenWidth,screenHeight]
        #myCanvas.create_polygon(tri1points, outline=None, fill='#ef2497')

        scrHeight = window.winfo_height()
        scrWidth = window.winfo_width()

        #playRecAudioImage = PhotoImage(file = __file__[0:__file__.rfind('\\')] + "\\png\\Record_NotPress.png")
        #playRecAudioImage = PhotoImage(file =r"C:\\Users\\livezeycorrw\\VSWorkspace\\SoftwareEngFinal\\Compugene_Project\\png\\Record_NotPress.png") 
        self.playRecAudioImage=PhotoImage(file =".\\png\\Record_NotPress.png")
        self.playRecAudioButton = Button(text="RECORD", image=self.playRecAudioImage, borderwidth=0, background='white',activebackground='white')
        self.playRecAudioButton.place(relx=.46, rely=.59, width=118, height=114)
        self.playRecAudioButton.configure(command= lambda : self.playRecAudio(self.playRecAudioButton))
        self.playRecAudioButton.bind('<ButtonPress>',self.changePlayRecAudioLook)

        self.reverseAudioImage=PhotoImage(file =".\\png\\Reverse_NotPress.png")
        self.reverseAudioButton=Button(image=self.reverseAudioImage, command = lambda : setReverse(), borderwidth=0, background='white',activebackground='white')
        self.reverseAudioButton.place(relx=.56, rely=.59, width=70, height=89)
        self.reverseAudioButton.bind('<ButtonPress>',self.changeReverseAudioLook)
        
        self.processAudioImage=PhotoImage(file =".\\png\\Process_Audio_NotPress.png")
        self.processAudioButton = Button(image=self.processAudioImage, command=lambda : processAudio(), borderwidth=0, background='white',activebackground='white')
        self.processAudioButton.place(relx=.3, rely=.59, width=192, height=63)
        self.processAudioButton.bind('<ButtonPress>',self.changeProcessAudioLook)

        self.deleteAudioImage=PhotoImage(file =".\\png\\Delete_Recording_NotPress.png")
        self.deleteAudioButton = Button(image=self.deleteAudioImage, command= lambda : deleteAudio(self.playRecAudioButton), borderwidth=0, background='white',activebackground='white')
        self.deleteAudioButton.place(relx=.04, rely=.04, width=137, height=114)
        self.deleteAudioButton.bind('<ButtonPress>',self.changeDeleteAudioLook)

        self.exportAudioImage = PhotoImage(file =".\\png\\Export_NotPress.png")
        self.exportAudioButton = Button(image = self.exportAudioImage, command=lambda : exportAudio(), borderwidth=0, background='white',activebackground='white')
        self.exportAudioButton.place(relx=.76, rely=.85, width=192, height=63)
        self.exportAudioButton.bind('<ButtonPress>',self.changeExportAudioLook)
        
        audioProgressBar = ttk.Progressbar(mode="determinate", orient="horizontal").place(relx=.2, rely=.52, relheight=.05, relwidth=.6)
        
        volumeSlider = Scale(from_=-24, to=24, orient=HORIZONTAL, resolution=3, variable=self.vol)
        volumeSlider.config(bg='white', highlightbackground='white',troughcolor='#ef2497')
        volumeSlider.place(relx=.05, rely=.72, relheight=.08, relwidth=.27)
        volumeSlider.set(0)
        pitchSlider = Scale(from_=.005, to=5, orient=HORIZONTAL, resolution=.005, variable=self.pitch)
        pitchSlider.config(bg='white',highlightbackground='white',troughcolor='#e802c1',)
        pitchSlider.place(relx=.05, rely=.89, relheight=.08, relwidth=.27)
        pitchSlider.set(1)
        
        myFont = font.Font(family="Helvetica", size=16, weight='bold', slant='italic')
        volumeLabel = Label(text="Volume (±db)", font=myFont)
        volumeLabel.config(bg='white')
        volumeLabel.place(relx=.04, rely=.65)
        pitchLabel = Label(text="Pitch (Hz)", font=myFont)
        pitchLabel.config(bg='white')
        pitchLabel.place(relx=.04, rely=.82)
        sampleRates = ["48k","44.1k", "24k","22.05k","12k","11.025k", "6k","5.5125k", "3k", "2.75625k"]
        bitDepths = ["16","8"]
        inputDevices = self.rec44k.getInputDevices() 
        self.rec48k.getInputDevices()
        outputDevices = self.looper.getOutputDevices()

        menuFont = font.Font(family="Helvetica", size=14, weight='bold')
        smallMenuFont = font.Font(family="Helvetica", size=12, weight='bold')
        sampleRateInitial = StringVar()
        sampleRateInitial.set("Sample Rate")
        sampleRateMenu = OptionMenu(window,sampleRateInitial,*sampleRates, command=self.selectSample)
        sampleRateMenu.config(bg='#ef2497', fg='black', borderwidth=0, highlightbackground="#d72697", font=menuFont)
        sampleRateMenu["menu"].config(bg='#6a0047', fg='white', borderwidth=0, font=smallMenuFont)
        sampleRateMenu.place(relx=.15, rely=.04, relwidth=.15, relheight=.1)

        bitDepthInitial = StringVar()
        bitDepthInitial.set("Bit Depth")
        bitDepthMenu = OptionMenu(window,bitDepthInitial,*bitDepths, command=self.selectDepth)
        bitDepthMenu.config(bg='#e802c1', fg='black', borderwidth=0, highlightbackground="#c70bb6", font=menuFont)
        bitDepthMenu["menu"].config(bg='#630065', fg='white', borderwidth=0, font=smallMenuFont)
        bitDepthMenu.place(relx=.32, rely=.04, relwidth=.15, relheight=.1)
        
        inputDeviceInitial = IntVar()
        inputDeviceInitial.set("Default Input")
        inputDeviceMenu = OptionMenu(window,inputDeviceInitial,*inputDevices, command=self.selectInput)
        inputDeviceMenu.config(bg='#ef2497', fg='black', borderwidth=0, highlightbackground="#d72697", font=menuFont)
        inputDeviceMenu["menu"].config(bg='#6a0047', fg='white', borderwidth=0, font=smallMenuFont)
        inputDeviceMenu.place(relx=.49, rely=.04, relwidth=.15, relheight=.1)
        
        outputDeviceInitial = IntVar()
        outputDeviceInitial.set("Default Output")
        outputDeviceMenu = OptionMenu(window,outputDeviceInitial,*outputDevices, command=self.looper.setDefaultOutput)
        outputDeviceMenu.config(bg='#e802c1', fg='black', borderwidth=0, highlightbackground="#c70bb6", font=menuFont)
        outputDeviceMenu["menu"].config(bg='#630065', fg='white', borderwidth=0, font=smallMenuFont)
        outputDeviceMenu.place(relx=.66, rely=.04, relwidth=.15, relheight=.1)

        rDecal = PhotoImage(file=".\\png\\Right_Decal.png")
        rightDecalLabel = Label(window,image=rDecal)
        rightDecalLabel.configure(background='white')
        rightDecalLabel.place(x=0,rely=0,width=196,height=531)

        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()

    def selectSample(self,selection):
        if selection == "Sample Rate":
            self.df="1"
            self.is_44k = True
        elif selection == "44.1k":
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
        if selection == "Bit Depth":
            self.bd="16"
        elif selection == "16":
            self.bd="16"
        elif selection == "8":
            self.bd="8"
        else:  
            print("Not valid sample rate")

    def selectInput(self,selection): 
        self.rec44k.setRecorderInput(selection)
        self.rec48k.setRecorderInput(selection)

    def getAudio(self):
        return self.has_audio

    def getPlaying(self):
        return self.is_playing

    def getRecording(self):
        return self.is_recording


if __name__ == '__main__':
    myGui = GUIWindow()
    myGui.makeGuiWindow()