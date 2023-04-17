
import wave
import pyaudio


class looper:
	
	def __init__(self):
		return
		
	def play_audio(self, wf, p, stream, gui): #end playing thread
		CHUNK = 1024
		while (gui.getPlaying() and len(data := wf.readframes(CHUNK))):  # Requires Python 	3.8+ for :=
			stream.write(data)

	def loop_audio(self, filename, gui):
		with wave.open(filename, 'rb') as wf:
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)
			
			while gui.getPlaying():
				self.play_audio(wf, p, stream, gui)
				wf = wave.open(filename, 'rb')				
			stream.close()
			p.terminate()
