import stk.python27bridge
import stk.events
import stk.services
import dance.dances as dances
import speech.speechrec as speechrec
import pose_detection.human_pose_detection as posedet
import time as t
from transformers import pipeline
import os
import numpy as np
from pygame import mixer
import re
import sys
import pyttsx3

# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class NaoDanceTutor:
    """ Main Nao class, from here all other classes are instantiated. """
    THRESHOLD = 0.3 # placeholder
    DANCE_TIMES = {'dab':8, 'airguitar':12, 'sprinkler':8}  # TODO: MEASURE ON NAO AND CHANGE ACCORDINGLY
    REF_FILES = [r"C:\Users\thoma\Documents\Studie\M1\HRI\ref_imgs\dab_ref.jpg", #dab
                  r"C:\Users\thoma\Documents\Studie\M1\HRI\ref_imgs\guitar_ref_2.jpg", # air_guitar
                   r"C:\Users\thoma\Documents\Studie\M1\HRI\ref_imgs\sprinkler_ref_2.jpg"] # sprinkler
    # REF_FILES = [r"C:\Users\luukn\OneDrive\Afbeeldingen\not_shit.jpg", 
    #              r"C:\Users\luukn\OneDrive\Afbeeldingen\not_shit.jpg",
    #              r"C:\Users\luukn\OneDrive\Afbeeldingen\not_shit.jpg"]
    SPEAK = False # for simulation


    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)

        # Initialize class instances
        self.dances = dances.Dances()
        self.speechrec = speechrec.SpeechRecognition(self.s)
        self.pose_detector = posedet.PoseDetector(dance_names=list(self.DANCE_TIMES.keys()),
                                                  ref_files=self.REF_FILES, 
                                                  nr_pics=3, verbose=True) 
        self.error_threshold = 50
        # self.engine = pyttsx3.init()
        # voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', voices[1].id)

    # def play_music(self, file, start=0):
    #     # Initialize the mixer
    #     mixer.init()

    #     # Load and play the audio file
    #     mixer.music.load(os.path.join(os.getcwd(), file).replace("\\", "/"))
    #     mixer.music.play(start=start)  # start=64 for funkytown.mp3

    def init_music(self, file):
        mixer.init()
        mixer.music.load(file)
        # Play the music and pause immideately
        mixer.music.play(-1)
        mixer.music.pause()

    def pause_music(self, fade_duration=1, stop=False):
        for i in range(100, -1, -1):
            mixer.music.set_volume(i / 100.0)
            t.sleep(fade_duration / 100.0)  # Sleep to simulate fading out over time
        if stop:
            mixer.music.stop()
        else:
            mixer.music.pause()
 
    def start_music(self, fade_duration=1):
        mixer.music.unpause() 
        for i in range(-1, 100, 1):
            mixer.music.set_volume(i / 100.0)
            t.sleep(fade_duration / 100.0) 

    def get_speech_time(self, text, wpm=155):
        nr_words = len(text.split())
        return nr_words/(wpm/60)

    def say(self, message, wait=True):
        try:
            self.s.ALTextToSpeech.say(message)
            if wait:
                if self.SPEAK:
                    self.engine.say(message)
                    self.engine.runAndWait()
                else:
                    est_time = self.get_speech_time(message)
                    print('estimated speech time: ', est_time)
                    t.sleep(est_time)
        except Exception as e:
            print(f"Error in say_message: {e}")

    def perform_dance(self, dance_type, multiplier=3, wait=True, get_time=False):
        self.start_music()
        dance_move = getattr(self.dances, dance_type)(multiplier=multiplier)
        self.s.ALMotion.angleInterpolationBezier(*dance_move)
        if wait:
            t.sleep(self.DANCE_TIMES[dance_type])
        if get_time:
            return self.DANCE_TIMES[dance_type]
        self.pause_music()
        
    def get_desired_move(self):
        valid_move = False
        i = 0
        while valid_move is False:
            if i == 0:
                self.say("Alright! Would you like to learn how to dab, a sprinkler or an air guitar?")
            else:
                self.say("Sorry, I didn't understand. Would you like to learn how to dab, a sprinkler or an air guitar?")
            input = self.speechrec.whispermini(3.0)

            if 'dab' in input.lower() or 'deb' in input.lower():
                dance = 'dab'
                valid_move = True
            if 'air' in input.lower() or 'guitar' in input.lower():
                dance = 'airguitar'
                valid_move = True
            if 'sprinkler' in input.lower() or 'sprinter' in input.lower():
                dance = 'sprinkler'
                valid_move = True

            i+=1
        
        return dance

    def teach_move(self):
        dance = self.get_desired_move()
        self.say(f"Sure thing! Let me teach you how to do a {dance}! Watch how I do it.")
        self.perform_dance(dance)    # automatically waits for dance to finish, set wait=False to not wait
        self.say("Now you try to do it!")
        
        successful_attempts, nr_errors = 0, 0
        while successful_attempts < 2:
            self.say("Are you ready?")
            x = False
            while x is False:
                input = self.speechrec.whispermini(3.0)
                print('input: ', input)
                if 'yes' in input.lower():
                    x = True
                if 'stop' in input.lower():
                    return
            self.say("One, two, three!")

            self.start_music()

            # Captures images and stores them
            self.pose_detector.take_pics()
            # Evaluates the captured images and returns the best error and image id
            smallest_error, best_image, best_mirrored = self.pose_detector.best_fitting_image_error(dance)
            self.pause_music()

            if smallest_error < self.error_threshold:
                if successful_attempts < 1:
                    self.say("Amazing! Let's try it again!")
                successful_attempts += 1
            else:
                successful_attempts = 0
                nr_errors += 1
                if (nr_errors % 2) == 0:
                    self.error_threshold += 10
                
                worst_error_bodypart = self.pose_detector.biggest_mistake(best_image, dance, best_mirrored)
                self.say(f"Nice try! But I think you can do it better. I'll show you again. Pay attention to my {worst_error_bodypart}")
                self.perform_dance(dance)      # automatically waits
                self.say("And now you again.")

            # check if participant still there
            if not self.pose_detector.detect_motion(threshold=100, detection_time=5, incremental=False):
                self.say("It seems like you left. I would love it if you would come back for some dancing.")
                if self.pose_detector.detect_motion(detection_time=10):
                    self.say("Welcome back! Let's continue.")
                else:
                    self.init_music("sound/EverybodyHurts.mp3")
                    self.start_music()
                    self.say("I guess you're not coming back, I will go cry now.")
                    t.sleep(20)
                    sys.exit()

        self.say("Good job! You've learned how to do the dab!")

    def look_for_moves(self, current_dance):
        for dance in self.DANCE_TIMES.keys():
                error, _, _ = self.pose_detector.best_fitting_image_error(dance)
                if error < self.error_threshold:
                    self.s.ALMotion.stopMove()
                    self.say(f'Nice {dance}! Keep up the good work', wait=True) # TODO: does this check the same image for each dance?
                    self.perform_dance(current_dance)
    
    def dance_together(self):
        dance = 'dab'
        self.say("Alrighty! Are you ready?")
        self.say("Here we go!")

        # Play music and dance
        #self.play_music("sound/Funkytown.mp3")
        self.start_music()
        dance_time_dab = self.perform_dance(dance, wait=False, get_time=True) # perform next code while dancing, and retrieve est time
        dance_time_guitar = self.perform_dance('airguitar', wait=False, get_time=True)
        dance_time_sprinkler = self.perform_dance('sprinkler', wait=False, get_time=True)


        # Check for dance moves and praise if executed correctly
        start_time = t.time()
        while t.time() - start_time < (dance_time_dab+dance_time_guitar +dance_time_sprinkler):  # loop for time it takes for Nao to perform dance
            self.pose_detector.take_pics()
            self.look_for_moves(dance)   

        # Stop leftover dance caused by starting new dance after stopping in look_for_moves()
        self.ALMotion.stopMove()
        self.pause_music()

        self.say("Wow, that was fun! I'm a bit tired now to be honest.")

    def extract_name(self, text):
        # Extracts name from inputs like "My name is Peter" or "Peter"
        match = re.search(r"\b(?:my name is|name's|i am|i'm|my name's)?\s*(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
        return None
    
    def introduction(self):
        if self.pose_detector.detect_motion(incremental=30):
            self.say("Hi there! What's your name?")
            
            got_name = False
            while got_name is False:
                name = self.extract_name(self.speechrec.whispermini(3.0))
                if name:
                    got_name = True
                else:
                    self.say("I'm sorry, I didn't get your name. Please say it again.")

            self.say(f"Hi {name}! My name is Nao, I am here to teach you some cool moves, but most importantly: to have fun together!")
            self.say("First off, you can choose whether you want to learn a dancemove, or to just dance together. What would you prefer?")

    def scenario(self):
        self.init_music('sound/boogie_bot_shuffle.mp3')
        stop = False
        counter = 0
        while stop is False:
            if counter != 0 and not misunderstand:
                self.say("Would you like to learn another move, dance together or stop?")
            

            input = self.speechrec.whispermini(3.0)
            print('input: ', input)

            if 'learn' in input.lower() or 'teach' in input.lower():
                self.teach_move()
            if 'dance' in input.lower() or 'together' in input.lower():
                self.dance_together()
            if 'stop' in input.lower() or 'quit' in input.lower():
                self.say("Alright, thanks a lot for joining, I had a lot of fun! I hope to see you again!")
                stop = True
            else:
                self.say("I'm sorry, I didn't understand that. Could you please say again if you would like to dance together or learn a move?")
                misunderstand = True

            counter += 1    

    def main(self):
        self.introduction()
        self.scenario()
        
        # print('dab')
        # self.perform_dance('dab', 2.5)
        # print('airguitar')
        # self.perform_dance('airguitar', 2.5)
        # print('sprinkler')
        # self.perform_dance('sprinkler', 2.5)
  
if __name__ == "__main__":
    nao = NaoDanceTutor()
    nao.main()


