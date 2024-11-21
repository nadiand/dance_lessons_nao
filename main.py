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

# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class NaoDanceTutor:
    """ Main Nao class, from here all other classes are instantiated. """
    
    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)

        # Initialize class instances
        print('checkpoint dance')
        self.dances = dances.Dances()
        print('checkpoint speechrec')

        self.speechrec = speechrec.SpeechRecognition(self.s)
        print('checkpoint posedet')

        self.pose_detector = posedet.PoseDetector(ref_file=r"C:\Users\thoma\Documents\Studie\M1\HRI\dab.jpg", nr_pics=3, verbose=True) # verbose=True????
        self.error_threshold = 50

    def say(self, message):
        try:
            self.s.ALTextToSpeech.say(message)
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
        dab = self.dances.dab(multiplier=3)
        self.s.ALMotion.angleInterpolationBezier(*dab)
        self.say("Now you try to do it!")
        t.sleep(10)
        
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
            t.sleep(3)
            # Captures images and stores them
            self.pose_detector.take_pics()
            # Evaluates the captured images and returns the best error and image id
            smallest_error, best_image = self.pose_detector.best_fitting_image_error()

            if smallest_error < self.error_threshold:
                if successful_attempts < 1:
                    self.say("Amazing! Let's try it again!")
                successful_attempts += 1
            else:
                successful_attempts = 0
                nr_errors += 1
                if (nr_errors % 2) == 0:
                    self.error_threshold += 10
                
                worst_error_bodypart = self.pose_detector.biggest_mistake(best_image)
                self.say(f"Nice try! But I think you can do it better. I'll show you again. Pay attention to my {worst_error_bodypart}")
                dab = self.dances.dab(multiplier=3)
                self.s.ALMotion.angleInterpolationBezier(*dab)
                t.sleep(8)
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
    
    def introduction(self):
        print(" checkpoint 3")

        if self.pose_detector.detect_motion():
            self.say("Hi there! What's your name?")
            
            name = self.speechrec.whispermini(3.0)
            print('name:', name)
            # TODO: make sure it says only name if it detects "my name is .."
            self.say(f"Hi {name}! My name is Nao, I am here to teach you some cool moves, but most importantly: to have fun together!")
            self.say("First off, you can choose whether you want to learn a dancemove, or to just dance together. What would you prefer?")
            t.sleep(15) # prevent from running next code before Nao is finished talking
        print(" checkpoint 4")
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
    print(" checkpoint 1")
    nao = NaoDanceTutor()
    print(" checkpoint 2")
    nao.main()


