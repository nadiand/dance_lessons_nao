import time as t
import speech_recognition as sr
from transformers import pipeline
import librosa

class SpeechRecognition:
    MIC = 0
    DEVICE = "cpu" 
    MODEL_NAME = "openai/whisper-tiny.en"  
    BEEP = True

    def __init__(self, s):
        self.r = sr.Recognizer()    
        self.r.energy_threshold = 4000
        self.s = s

        self.pipe = pipeline(
			task="automatic-speech-recognition",
			model=self.MODEL_NAME,
			# language="en",
			chunk_length_s=2,
			device=self.DEVICE,
		)

        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language="en", task="transcribe")
    
    def speech_recognize(self, time): 
        with sr.Microphone(self.MIC) as source:
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
        
    def whispermini(self, time):
        with sr.Microphone(self.MIC) as source:
            self.r.adjust_for_ambient_noise(source)
            if self.BEEP is True:
                self.s.ALAudioPlayer.playSine(1000, 10, 1.0, 0.5)
            print('Listening for audio...')
            audio = self.r.listen(source, phrase_time_limit=time)
            if self.BEEP is True:
                self.s.ALAudioPlayer.playSine(2000, 10, 1.0, 0.5)
            print('Audio succesfully captured! Now saving and processing audio...')

            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())

            wav, rate = librosa.load("microphone-results.wav")
            wav = librosa.resample(wav, orig_sr=rate, target_sr=16000)

            words = self.pipe(wav, batch_size=32)
            print("WHISPER:", words)
            return words['text']