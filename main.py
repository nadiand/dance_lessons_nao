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

# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class NaoDanceTutor:
    """ Main Nao class, from here all other classes are instantiated. """
    THRESHOLD = 0.3 # placeholder
    
    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)

        # Initialize class instances
        self.dances = dances.Dances()
        self.speechrec = speechrec.SpeechRecognition(self.s)
        # self.pose_detector = posedet.PoseDetector(dance_names=["dab"],
        #                                           ref_files=[r'C:/Users/luukn/OneDrive/Afbeeldingen/not_shit.jpg'], 
        #                                           nr_pics=3, verbose=True) 
        self.error_threshold = 50

    def get_speech_time(self, text, wpm=170):
        nr_words = len(text.split())
        return nr_words/(wpm/60)
    
    def get_move_time(self, move):
        if move=='dab':
            return 8   # change accordingly
        if move=='airguitar':
            return 10  # change accordingly
        
    def get_combined_time(self, move, text):
        return self.estimate_move_time(move) + self.get_speech_time(text)

    def say(self, message):
        try:
            self.s.ALTextToSpeech.say(message)
            est_time = self.get_speech_time(message)
            print('estimated speech time: ', est_time)
            t.sleep(est_time)
        except Exception as e:
            print(f"Error in say_message: {e}")
        
    def test_dance(self):
        dab = self.dances.dab(multiplier=3)
        self.s.ALMotion.angleInterpolationBezier(*dab)
        air_guitar = self.dances.air_guitar(multiplier=2)
        self.s.ALMotion.angleInterpolationBezier(*air_guitar)
        dance = self.dances.dance_move(multiplier=3)
        self.s.ALMotion.angleInterpolationBezier(*dance)

    def teach_move(self):
        self.say("Alright! Let me teach you how to do a dab! Watch how I do it.")
        dance = "dab"
        dab = self.dances.dab(multiplier=3)
        self.s.ALMotion.angleInterpolationBezier(*dab)
        t.sleep(self.estimate_move_time(dance))  # is this needed?
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
            self.say("One, two, three!")
            # Captures images and stores them
            self.pose_detector.take_pics()
            # Evaluates the captured images and returns the best error and image id
            smallest_error, best_image, best_mirrored = self.pose_detector.best_fitting_image_error(dance)

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
                dab = self.dances.dab(multiplier=3)
                self.s.ALMotion.angleInterpolationBezier(*dab)
                t.sleep(self.estimate_move_time(dance))
                self.say("And now you again.")

        self.say("Good job! You've learned how to do the dab!")

    def play_music(self, file):
        # Initialize the mixer
        mixer.init()

        # Load and play the audio file
        mixer.music.load(os.path.join(os.getcwd(), file).replace("\\", "/"))
        mixer.music.play()  # start=64 for funkytown.mp3
    
    def dance_together(self):
        self.say("Alrighty! Are you ready?")
        t.sleep(2)
        self.say("Here we go!")
        # play music and dance
        self.play_music("sound/Funkytown_cut.wav")
        self.test_dance()

        #stop music when dancing done
        #mixer.music.stop()

    def extract_name(self, text):
        # Extracts name from inputs like "My name is Peter" or "Peter"
        match = re.search(r"\b(?:my name is|name's|i am|i'm)?\s*(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
        return None
    
    def introduction(self):
        if self.pose_detector.detect_motion():
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
        x = False
        while x is False:
            input = self.speechrec.whispermini(3.0)
            print('input: ', input)
            if 'learn' in input or 'teach' in input:
                self.teach_move()
                x = True
            if 'dance' in input or 'together' in input:
                self.dance_together()
                x = True
    
    def main(self):
        self.introduction()
        self.scenario()
  
if __name__ == "__main__":
    nao = NaoDanceTutor()
    nao.main()


