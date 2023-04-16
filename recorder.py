
import subprocess
import sys
import wave
import pyaudio

#

class recorder: #give decimate
	master_rec = None
	processed_rec = None
	recorded = False
	
	CHUNK = int(1024/16)
	FORMAT = pyaudio.paInt16
	CHANNELS = 1 if sys.platform == 'darwin' else 2
	RATE = int(44100) ##Default master sample rate
	FILENAME="output.wav"
	
	def __init__(self, master_framerate):
		if (master_framerate!=44100):
			self.RATE=master_framerate
	
	def record(self, gui, bitdepth, decimation):
		self.o_record(gui)
		self.recorded=True
		self.master_rec=self.FILENAME
		self.processed_rec="decimated.wav"
		self.decimate(self.processed_rec, bitdepth, decimation)
	
	##Records a .wav file using registered input at 44.1k
	def o_record(self, gui):

		with wave.open(self.FILENAME, 'wb') as wf:
			p = pyaudio.PyAudio()
			wf.setnchannels(self.CHANNELS)
			wf.setsampwidth(p.get_sample_size(self.FORMAT))
			wf.setframerate(self.RATE)

			stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True)

			print('Recording...')
			while(gui.getRecording()):
				wf.writeframes(stream.read(self.CHUNK))
			print('Done')

			stream.close()
			p.terminate()
	
	#Creates new file that with sample rate reduced by given factor (df) and with selected bit-depth (bd)   
	def decimate(self, filename, bd, df):	
		
		r = open("userdata.txt", "r")
		SoxFilePath = r.read()
		r.close()

		print(filename)
		print(bd)
		print(df)
		
		try:
			subprocess.call([SoxFilePath, '-V1', self.FILENAME, '-b', str(bd), filename, 'downsample', str(df)], stdout=subprocess.PIPE)
		except:
			#Finds sox's location when it is missing, alters it based on the assumption of relative directories
			SoxFilePath = __file__[0:__file__.rfind('\\')] + "\\sox-14-4-2\\sox.exe"

			w = open("userdata.txt", "w")
			w.write(SoxFilePath)
			w.close()
			#print(SoxFilePath)

			subprocess.call([SoxFilePath, '-V1', self.FILENAME, '-b', str(bd), filename, 'downsample', str(df)], stdout=subprocess.PIPE)
		return 0

	def has_recorded(self):
		return self.recorded
	