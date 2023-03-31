import os
import wave
import sys
import subprocess
from time import sleep
try: #This will eventually be moved to an installation script for all relevant libraries
	import pyaudio
except: 
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyaudio'])
import gui
'''
This script records a .wav file of a provided length using the currently registered audio input.
Afterwards it applies a decimation process to chop the sample rate and bit depth. 
'''

CHUNK = int(1024/16)
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = int(44100)
FILENAME='output.wav'

##Records a .wav file using registered input at 44.1k
def record(gui):

	with wave.open(FILENAME, 'wb') as wf:
		p = pyaudio.PyAudio()
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)

		stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

		print('Recording...')
		while(gui.getRecording()):
			wf.writeframes(stream.read(CHUNK))
		print('Done')
		
		stream.close()
		p.terminate()

#Creates new file that with sample rate reduced by given factor (df) and with selected bit-depth (bd)   
def decimate(filename, bd, df):	

	r = open("userdata.txt", "r")
	SoxFilePath = r.read()
	r.close()
	#print(SoxFilePath)	

	###Run sox.exe at verbose level 1 (-V1) only errors will be outputted to std-out	
	try:
		subprocess.call([SoxFilePath, '-V1', FILENAME, '-b', bd, filename, 'downsample', df], stdout=subprocess.PIPE)
	except:
		#Finds sox's location when it is missing, alters it based on the assumption of relative directories
		SoxFilePath = __file__[0:__file__.rfind('\\')] + "\\sox-14-4-2\\sox.exe"

		w = open("userdata.txt", "w")
		w.write(SoxFilePath)
		w.close()
		#print(SoxFilePath)

		subprocess.call([SoxFilePath, '-V1', FILENAME, '-b', bd, filename, 'downsample', df], stdout=subprocess.PIPE)

	return 0

def recordAudio(gui):
	record(gui)
	decimate('newfile.wav', '8', '2')