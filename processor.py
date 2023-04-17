#look at processAudio to make necessary modifications

#then move to GUI

from pydub import AudioSegment

class processor:
	fwd = True
	speed = 1.0
	master_framerate = 44100
	audio = "None"
	master = "None"
	
	def __init__(self, master_framerate, filename):
		print("processor initialized")
		print(master_framerate)
		print(filename)
		if (master_framerate!=44100):
			self.master_framerate=master_framerate	
		audio = AudioSegment.from_wav(filename)
		self.audio=audio
		self.master=audio
	
	def alter_speed(self, audio, mult):
		octaves = 0.5
		#This variable changes the speed-> 1 is normal, 2 is twice as fast, .5 is half speed
		speed_control = float(mult)
		
		new_sample_rate = int(audio.frame_rate * (speed_control ** octaves))
		
		pitched_sound=audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
		
		pitched_sound = pitched_sound.set_frame_rate(self.master_framerate)
		self.audio=pitched_sound
		return pitched_sound

	def reverse(self, audio):
		audio = audio.reverse()
		self.fwd = not self.fwd
		return audio
		
	def trim(self, audio, start, end):
		# pydub does things in miliseconds
		start=int(float(start) * 1000)
		end=int(float(end) * 1000)

		audio = audio [start:end]
		self.audio=audio
		return audio

	def amplify(self, audio, amp):
		amp=int(amp)
		audio+=amp
		self.audio=audio
		return audio
	
	def get_audiosegment(self):
		return self.audio

	def get_master(self):
		return self.master
	
	def is_fwd(self):
		return self.fwd