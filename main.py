import stk.python27bridge
import stk.events
import stk.services
import dances
import speechrec
import time as t
from transformers import pipeline
import librosa
import threading
import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# import tensorflow 

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
        dance = self.dances.air_guitar(multiplier=0.5)
        self.s.ALMotion.angleInterpolationBezier(dance[0], dance[1], dance[2])

        dance = self.dances.dance_move()
        self.s.ALMotion.angleInterpolationBezier(dance[0], dance[1], dance[2])

    def motion_detected(self):
        """ IMPLEMENT """
        return True
    
    def teach_move(self):
        """ IMPLEMENT """
        self.test_dance()
    
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


