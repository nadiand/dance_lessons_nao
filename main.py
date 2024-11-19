import stk.python27bridge
import stk.events
import stk.services
import dance.dances
import speech.speechrec
import time as t
from transformers import pipeline
import librosa
import threading
import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# import tensorflow 

LANDMARK_NAMES = ['left elbow', 'right hip'] # placeholder values
THRESHOLD = 0.3 # placeholder

class NaoDanceTutor:
    """ Main Nao class, from here all other classes are instantiated. """
    
    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)

        # Initialize class instances
        self.dances = dances.Dances()
        self.speechrec = speechrec.SpeechRecognition(self.s)

    def say(self, message):
        try:
            self.s.ALTextToSpeech.say(message)
        except Exception as e:
            print(f"Error in say_message: {e}")
        
    def test_dance(self):
        dance = self.dances.dab(multiplier=0.5)
        self.s.ALMotion.angleInterpolationBezier(*dance)
        # dance = self.dances.air_guitar(multiplier=0.5)
        # self.s.ALMotion.angleInterpolationBezier(*dance)

        # dance = self.dances.dance_move()
        # self.s.ALMotion.angleInterpolationBezier(*dance)

    def motion_detected(self):
        """ IMPLEMENT """
        return True
    
    def teach_move(self):
        self.say("Alright! Let me teach you how to do air guitar! Watch how I do it.")
        self.test_dance()
        self.say("Now you try to do it!")
        
        successful_attempts = 0
        while successful_attempts < 3:
            self.say("One, two, three!")
            # TODO: call another function to record a vid
            # TODO: call another function to compare movement to reference and send back the errors for each landmark
            landmark_errors = [0.1, 0.3] # placeholder values
            if mean(landmark_errors) < THRESHOLD:
                successful_attempts += 1
                self.say("Amazing! Let's try it again together!")
            else:
                successful_attempts = 0
                worst_error = np.argmax(landmark_errors)
                self.say(f"Nice try! But I think you can do it better. I'll show you again. Pay attention to my {LANDMARK_NAMES[worst_error]}")
                self.test_dance()
                self.say("And now you again.")

        self.say("Good job! You've learned how to do air guitar!")
       
    
    def dance_together(self):
        """ IMPLEMENT """
        # Somehow need to get both commands simulatenous, using the .post function, how?
        self.s.ALAudioPlayer.playFile(os.path.join(os.getcwd(), "NaoBeat.wav").replace("\\", "/"))
        self.test_dance()

    
    def introduction(self):
        if self.motion_detected():
            self.say("Hi there!")
        t.sleep(2)                  # give time for response
        #name = nao.whispermini(3.0)['text']

        self.say("My name is Nao, I am here to teach you some cool moves, but most importantly: to have fun together!")
        self.say("First off, you can choose whether you want to learn a dancemove, or to just dance together. What would you prefer?")
        
    
    def scenario(self):
        #input = self.speechrec.whispermini(3.0)['text']
        input = "I want to dance"
        if "learn" in input:
            self.teach_move()
        else:
            self.dance_together()
    
    def main(self):
        self.introduction()
        self.scenario()

        

    
if __name__ == "__main__":
    nao = NaoDanceTutor()
    nao.main()


