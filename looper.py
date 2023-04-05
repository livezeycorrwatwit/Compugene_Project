#look at testPlay and playAudio to make necessary modifications

#then move to GUI

import wave
import pyaudio


class looper:
	
	def __init__(self):
		return
		
	def play_audio(self, wf, p, stream):
		CHUNK = 1024
		while len(data := wf.readframes(CHUNK)):  # Requires Python 	3.8+ for :=
			stream.write(data)

	def loop_audio(self, filename, repeats):
		with wave.open(filename, 'rb') as wf:
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)
					
			repeats = int(repeats)
			
			while repeats>0:
				self.play_audio(wf, p, stream)
				wf = wave.open(filename, 'rb')
				repeats-=1
				
			stream.close()
			p.terminate()
	
	def loop_until_flag(self, filename, flag):
		with wave.open(filename, 'rb') as wf:
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)
					
			repeats = int(repeats)
			
			while repeats>flag:
				self.play_audio(wf, p, stream)
				wf = wave.open(filename, 'rb')
				repeats-=1
				
			stream.close()
			p.terminate()