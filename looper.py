
import wave
import pyaudio


class looper:
	
	def __init__(self):
		self.outputs = None
		self.output_index = None
		return

	def getOutputDevices(self):
		p = pyaudio.PyAudio()
		host = p.get_host_api_info_by_index(0)
		n = host.get('deviceCount')

		self.outputs = {}

		for i in range(0, n):
			if(p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
				self.outputs[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i

		return self.outputs #return dictionary of name -> index

	def setDefaultOutput(self, x):
		print(type(self.outputs[x]))
		print(self.outputs[x])
		self.output_index = self.outputs[x]
		
	def play_audio(self, wf, p, stream):
		CHUNK = 1024
		while len(data := wf.readframes(CHUNK)):  # Requires Python 	3.8+ for :=
			stream.write(data)

	def loop_audio(self, filename, gui):
		with wave.open(filename, 'rb') as wf:
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True,
							output_device_index=self.output_index)
			while gui.getPlaying():
				self.play_audio(wf, p, stream)
				wf = wave.open(filename, 'rb')				
			stream.close()
			p.terminate()
