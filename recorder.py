
import subprocess
import sys
import wave
import pyaudio


#look at testRecord and recordScript to make necessary modifications

#then move to GUI

class recorder:
	master_rec = None
	processed_rec = None
	recorded = False
	
	CHUNK = int(1024/16)
	FORMAT = pyaudio.paInt16
	CHANNELS = 1 if sys.platform == 'darwin' else 2
	RATE = int(44100) ##Master sample rate
	FILENAME="output.wav"
	
	def __init__(self, master_framerate):
		if (master_framerate!=44100):
			self.RATE=master_framerate
	
	def record(self, length, bitdepth, decimation):
		self.o_record(length)
		self.recorded=True
		self.master_rec=self.FILENAME
		self.processed_rec="decimated.wav"
		self.decimate(self.processed_rec, bitdepth, decimation)

	##Records a .wav file using registered input at 44.1k
	def o_record(self, length):
		if length.isnumeric():
			length = int(length)
		else:
			length=5
		with wave.open(self.FILENAME, 'wb') as wf:
			p = pyaudio.PyAudio()
			wf.setnchannels(self.CHANNELS)
			wf.setsampwidth(p.get_sample_size(self.FORMAT))
			wf.setframerate(self.RATE)

			stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True)

			print('Recording...')
			for _ in range(0, self.RATE // self.CHUNK * length):
				wf.writeframes(stream.read(self.CHUNK))
			print('Done')
		

			stream.close()
			p.terminate()

	#Creates new file that with sample rate reduced by given factor (df) and with selected bit-depth (bd)   
	def decimate(self, filename, bd, df):	
		##Get up filepath where sox.exe is
		FilePath=r"C:\Users\vidali\Desktop\AudioTools\sox-14-4-2"
		
		print(filename)
		print(bd)
		print(df)
		
		##Run sox.exe at verbose level 1 (-V1) only errors will be outputted to std-out	
		subprocess.call(['sox.exe', '-V1', self.FILENAME, '-b', bd, filename, 'downsample', df], stdout=subprocess.PIPE)
		return 0
	
	def has_recorded(self):
		return self.recorded
	