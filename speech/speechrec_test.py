import stk.python27bridge
import stk.events
import stk.services
import speech_recognition as sr
import time as t
from transformers import pipeline
import librosa


class DancerNAO():

	def __init__(self, ip, port, s):
		self.ip = ip
		self.port = port
		self.r = sr.Recognizer()
		self.r.energy_threshold = 4000
		self.s = s

		DEVICE = "cpu"
		MAX_DURATION_IN_SECONDS = 30
		MODEL_NAME = "openai/whisper-tiny.en"

		self.pipe = pipeline(
			task="automatic-speech-recognition",
			model=MODEL_NAME,
			# language="en",
			chunk_length_s=2,
			device=DEVICE,
		)

		self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language="en", task="transcribe")
		
	def speech_recognize(self, time):
		with sr.Microphone() as source:
			one = t.time()
			self.r.adjust_for_ambient_noise(source)
			two = t.time()
			print("mic on... start recording!")
			audio = self.r.listen(source, phrase_time_limit=time)
			print(audio.get_raw_data())
			print("done recording")
			three = t.time()

			# with open(r'C:\Users\thoma\Documents\Studie\M1\HRI\bridge\robot-jumpstarter-python3-master\python3\test.wav', 'wb') as f:
			# 	f.write(audio.get_wav_data())
			words = self.r.recognize_whisper(audio)
			four = t.time()
			print('Reconized words: ' + words)
			print("2-1: ", two - one )
			print("3-2: ", three - two )
			print("4-3: ", four - three )
			print("total time: ", four - one )
			



			return words
			

		# Alternative using Whisper from OpenAI's library
		# with sr.Microphone() as source:
		#	 print("Say something!")
		#	 audio = r.listen(source)
		#	 print ("Processing...")
		#	 client = OpenAI()
		#	 with open("microphone-results.wav", "wb") as f:
		#		 f.write(audio.get_wav_data())

		#	 with open("microphone-results.wav", "rb") as f:
		#		 transcript = client.audio.transcriptions.create(
		#		 model="whisper-1",
		#		 file=f,
		#		 response_format="text",
		#		 )
		# return transcript
	
	def whispermini(self, time):

		with sr.Microphone() as source:
			self.r.adjust_for_ambient_noise(source)
			self.s.ALAudioPlayer.playSine(1000, 10, 1.0, 0.5)
			audio = self.r.listen(source, phrase_time_limit=time)
			self.s.ALAudioPlayer.playSine(2000, 10, 1.0, 0.5)

			with open("microphone-results.wav", "wb") as f:
				f.write(audio.get_wav_data())

			wav, rate = librosa.load("microphone-results.wav")
			wav = librosa.resample(wav, orig_sr=rate, target_sr=16000)

			words = self.pipe(wav, batch_size=32)
			return words



	def create_proxy(self, name):
		
		proxy = self.s.ALProxy(name, self.ip, self.port)
		

		return proxy

	def say(self, text):
		self.s.ALTextToSpeech.say(text)

	def move(self, motion):
		# motion = self.s.ALMotion.setAngles('moveHead', 'HeadPitch', -0.6)
		if motion == "move head":
			self.s.ALMotion.setAngles('moveHead', 'HeadPitch', -0.6) 
		elif motion == "rest":
			self.s.ALMotion.rest()
			

class Python3NaoExample:
	def __init__(self):
		self.python27bridge = stk.python27bridge.Python27Bridge()
		self.events = stk.events.EventHelper(self.python27bridge)
		self.s = stk.services.ServiceCache(self.python27bridge)
		# self.events.connect("ALAnimatedSpeech/EndOfAnimatedSpeech", self.animated_speech_end)
		self.s.ALTextToSpeech.say("Willem has a beautiful left ear")
		# self.events.wait_for("Jantest/Test")
		# self.s.ALTextToSpeech.say("And this won't trigger until after a JanTest/Test event is fired (e.g. from Choregraphe)")
		  
		nao_ip = "192.168.0.103"
		port = 9559
		nao = DancerNAO(nao_ip, port, self.s)

		nao.say('Hi, i am a dancer!')

		while True:
			print("Waiting for Keyword")
			# prompt = nao.speech_recognize(3.0).lower()
			prompt = nao.whispermini(3.0)
			prompt = prompt['text']
			
			print("You said: " + prompt)
			if "dance" in prompt:
				nao.say("Yes sir")
				nao.move("move head")
			elif "chicken" in prompt:
				nao.say("you said chicken")
			elif "stop" in prompt:
				nao.say("Oki, bye")
				nao.move("rest")
				break
			else:
				nao.say("I do not understand")

	def animated_speech_end(self, args):
		print("Animated speech ended..")

		if args:
			print(args)

		self.events.disconnect("ALAnimatedSpeech/EndOfAnimatedSpeech")
		self.s.ALAnimatedSpeech.say("This is another test!")



if __name__ == "__main__":
	Python3NaoExample()
