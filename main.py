import stk.python27bridge
import stk.events
import stk.services
import dance.dances as dances
import speech.speechrec as speechrec
import pose_detection.human_pose_detection as posedet
import speech_alternatives as alter
import time as t
from transformers import pipeline
import os
import numpy as np
from pygame import mixer
import re
import sys
import pyttsx3
import random
import threading
import tkinter as tk

# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class NaoDanceTutor:
    """ Main Nao class, from here all other classes are instantiated. """
    THRESHOLD = 0.3 # placeholder
    DANCE_TIMES = {'dab':10, 'airguitar':16, 'sprinkler':17}  # TODO: MEASURE ON NAO AND CHANGE ACCORDINGLY
    REF_FILES = [r"C:\Users\luukn\OneDrive\Afbeeldingen\dab_ref.jpg", #dab
                 r"C:\Users\luukn\OneDrive\Afbeeldingen\guitar_ref_1.jpg", # air_guitar
                 r"C:\Users\luukn\OneDrive\Afbeeldingen\sprinkler_ref_1.jpg"] # sprinkler
    SPEAK = False # for simulation
    INTERACTIVE = False

    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)

        # Initialize class instances
        self.dances = dances.Dances()
        self.speechrec = speechrec.SpeechRecognition(self.s)
        self.speech_options = alter.SpeechAlternatives()
        self.pose_detector = posedet.PoseDetector(dance_names=list(self.DANCE_TIMES.keys()),
                                                  ref_files=self.REF_FILES, 
                                                  nr_pics=3, verbose=False) 
        self.error_threshold = 50
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

    def gui_stop(self):
        """ Tkinter GUI for stopping the program. """
        self.root = tk.Tk()
        self.root.title("Nao Dance Tutor Controller")

        stop_button = tk.Button(self.root, text="STOP", command=self.set_stop_flag, bg="red", fg="white", font=("Arial", 16))
        stop_button.pack(padx=20, pady=20)

        label = tk.Label(self.root, text="Click STOP to terminate the program", font=("Arial", 12))
        label.pack()

        # Start the Tkinter event loop
        self.root.mainloop()

    def set_stop_flag(self):
        """ Set the stop flag to True and close the Tkinter window. """
        print("\n[INFO] Stop button clicked. Terminating program.")
        self.stop_flag = True
        self.root.destroy()  # Close the Tkinter window

    def check_for_stop(self):
        """ Check if the program should stop and exit if necessary. """
        if self.stop_flag:
            print("Program terminated by researchers.")
            self.say("I'm sorry, but unfortunately we're out of time, thanks a lot for participating and I hope to see you again!", check=False)
            sys.exit()

    def init_music(self, file):
        mixer.init()
        mixer.music.load(file)
        # Play the music and pause immediately
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

    def get_speech_time(self, text, wpm=215):
        """ Estimate speech time of text given specified words per minute. """
        nr_words = len(text.split())
        return nr_words/(wpm/60)

    def say(self, message, wait=True, check=True):
        """ Make Nao speak and sleep for estimated amount of speech time. """
        try:
            if check:
                self.check_for_stop()
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

    def perform_dance(self, dance_type, multiplier=3, wait=True, get_time=False, pause_music=True):
        """ Perform dance_type and sleep until finished. """
        self.start_music()
        dance_move = getattr(self.dances, dance_type)(multiplier=multiplier)
        self.s.ALMotion.angleInterpolationBezier(*dance_move)
        if wait:
            t.sleep(self.DANCE_TIMES[dance_type])
        if get_time:
            return self.DANCE_TIMES[dance_type]
        if pause_music:
            self.pause_music()

    def find_movement(self):
        """ Check if participant still there. """
        if not self.pose_detector.detect_motion(threshold=100, detection_time=5, incremental=False):
            self.say(random.choice(self.speech_options.left_message))
            if self.pose_detector.detect_motion(detection_time=10):
                self.say(random.choice(self.speech_options.welcome_back))
            else:
                self.init_music("sound/EverybodyHurts.mp3")
                self.start_music()
                self.say(random.choice(self.speech_options.cry))
                t.sleep(20)
                sys.exit()
        
    def get_desired_move(self):
        """ Obtain move to teach. """
        valid_move = False
        i = 0
        while valid_move is False:
            if i == 0:
                self.say(random.choice(self.speech_options.desired_move))
            else:
                # if user wants another move give appropriate answer
                if 'another' in input.lower() or 'move' in input.lower() or 'else' in input.lower() or 'other' in input.lower():
                    self.say(random.choice(self.speech_options.desired_move_other)) 
                else:
                    self.say(random.choice(self.speech_options.desired_move_misunderstand))
            input = self.speechrec.whispermini()
            if input == '':
                self.find_movement()

            if 'dab' in input.lower() or 'deb' in input.lower() or 'dead' in input.lower() or 'dev' in input.lower() or 'depth' in input.lower() or 'DAP' in input.lower() or 'death' in input.lower():
                dance = 'dab'
                valid_move = True
            if 'air' in input.lower() or 'guitar' in input.lower():
                dance = 'airguitar'
                valid_move = True
            if 'sprinkler' in input.lower() or 'sprinter' in input.lower() or 'spring' in input.lower():
                dance = 'sprinkler'
                valid_move = True

            i+=1
        
        return dance
    
    def stop_learning(self, loop):
        """ Ask if participant still wants to continue learning every 2 loops. """
        if loop%2==0 and loop!=0:
                self.say(random.choice(self.speech_options.teach_loop_check))
                input = self.speechrec.whispermini()
                if input == '':
                    self.find_movement()
                if 'something' in input.lower() or 'else' in input.lower() or 'stop' in input.lower() or 'quit' in input.lower():
                    return True
        return False

    def teach_move(self, dance_interactive='dab'):
        """ Teach dance move in loop structure. """
        if self.INTERACTIVE:
            dance = self.get_desired_move()
            self.say(random.choice(self.speech_options.teach_intro(dance)))
        else:
            dance = dance_interactive
            self.say(random.choice(self.speech_options.teach_intro_non_interactive(dance)))
        self.perform_dance(dance)    # automatically waits for dance to finish, set wait=False to not wait
        self.say(random.choice(self.speech_options.teach_start))

        early_stop = False
        successful_attempts, nr_errors, loop = 0, 0, 0
        while successful_attempts < 2:
            if self.INTERACTIVE:
                if self.stop_learning(loop):
                    early_stop = True
                    break

            self.say(random.choice(self.speech_options.dance_together_intro))   

            # if self.INTERACTIVE:
            #     ready = False
            #     while ready is False:
            #         input = self.speechrec.whispermini()
            #         if input == '':  # stop everything if no audio detected
            #             self.find_movement()

            #         print('input: ', input)
            #         if 'yes' in input.lower() or 'ready' in input.lower():
            #             ready = True
            #         if 'stop' in input.lower() or 'no' in input.lower():
            #             return
            # else:
            t.sleep(2)  # if not interactive, just wait 2 seconds and then start
            self.say("One, two, three!")

            self.start_music()

            if self.INTERACTIVE:
                # Captures images and stores them
                self.pose_detector.take_pics()
                # Evaluates the captured images and returns the best error and image id
                smallest_error, best_image, best_mirrored = self.pose_detector.best_fitting_image_error(dance)
                self.pause_music()

                if smallest_error < self.error_threshold:
                    if successful_attempts < 1:
                        self.say(random.choice(self.speech_options.positive_feedback))
                    successful_attempts += 1
                else:
                    successful_attempts = 0
                    nr_errors += 1
                    if (nr_errors % 2) == 0:
                        self.error_threshold += 10
                    
                    worst_error_bodypart = self.pose_detector.biggest_mistake(best_image, dance, best_mirrored)
                    self.say(random.choice(self.speech_options.negative_feedback(worst_error_bodypart)))
                    self.perform_dance(dance)      # automatically waits
                    self.say(random.choice(self.speech_options.teach_resume))
            else:
                t.sleep(10)      
                self.pause_music()
                if loop==0:
                    self.say("Wow that was great! Let's try one more time.")
                successful_attempts+=1

            if self.INTERACTIVE:
                self.find_movement() # check if participant still there
            loop+=1

        if not early_stop:
            self.say(random.choice(self.speech_options.teach_end(dance)))

    def good_move_found(self, dance):
        """ Loop over all dances to see if performed participant dance matches to one of the saved ones, praise if yes. """
        error, _, _ = self.pose_detector.best_fitting_image_error(dance)
        if error < self.error_threshold:
            return True

    def perform_and_check_dance(self, dance):
        # Play music and dance
        dance_time = self.perform_dance(dance, wait=False, get_time=True, pause_music=False) # perform next code while dancing, and retrieve est time
        start_time = t.time()
        while t.time() - start_time < (dance_time):
            self.pose_detector.take_pics()
            if self.good_move_found(dance) and self.INTERACTIVE:
                self.say(random.choice(self.speech_options.dance_together_feedback(dance)))

    
    def dance_together(self):
        self.say(random.choice(self.speech_options.dance_together_intro))
        # if self.INTERACTIVE:
        #     ready = False
        #     while ready is False:
        #         input = self.speechrec.whispermini()
        #         if input == '':  # stop everything if no audio detected
        #             self.find_movement()

        #         print('input: ', input)
        #         if 'yes' in input.lower() or 'ready' in input.lower():
        #             ready = True
        #         if 'stop' in input.lower() or 'no' in input.lower():
        #             return
        # else:
        t.sleep(2)

        self.say(random.choice(self.speech_options.dance_together_start))

        # Check for dance moves and praise if executed correctly 
        for dance in self.DANCE_TIMES.keys():
            self.perform_and_check_dance(dance)

        self.pause_music()

        self.say(random.choice(self.speech_options.dance_together_end))


    def extract_name(self, text):
        """ Extract name from inputs like "My name is Peter" or "Peter". """
        match = re.search(r"\b(?:my name is|name's|i am|i'm|my name's)?\s*(\w+)", text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
        return None
    
    def introduction(self):
        """ Introduction of Nao. """
        input('Press key to start:)')
        if self.pose_detector.detect_motion(incremental=3):
            self.say(random.choice(self.speech_options.welcome_message))
            
            if self.INTERACTIVE:
                self.say(random.choice(self.speech_options.ask_name))
                got_name = False
                while got_name is False:
                    name = self.extract_name(self.speechrec.whispermini())
                    if name:
                        got_name = True
                    else:
                        self.say(random.choice(self.speech_options.not_understood_name))

                self.say(random.choice(self.speech_options.greetings(name)))
                self.say(random.choice(self.speech_options.intro_options))
 
    def scenario(self):
        """ Overall scenario loop. """
        self.init_music('sound/boogie_bot_shuffle.mp3')
        if self.INTERACTIVE:
            stop = False
            counter = 0
            while stop is False:
                if counter != 0 and not misunderstand:
                    self.say(random.choice(self.speech_options.scenario_options))
                

                input = self.speechrec.whispermini()
                if input == '': # stop everything if no audio detected
                    self.find_movement()

                if 'learn' in input.lower() or 'teach' in input.lower() or 'another' in input.lower():
                    self.teach_move()
                    misunderstand=False
                elif 'dance' in input.lower() or 'together' in input.lower() or 'freestyle' in input.lower() or 'desicator' in input.lower():
                    self.dance_together()
                    misunderstand=False
                elif 'stop' in input.lower() or 'quit' in input.lower():
                    self.say(random.choice(self.speech_options.end_message))
                    stop = True
                else:
                    self.say(random.choice(self.speech_options.scenario_misunderstood))
                    misunderstand = True

                counter += 1    
        else:
            self.say("Let's start with teaching you a cool dancemove!")
            self.teach_move(dance_interactive='dab')
            self.teach_move(dance_interactive='airguitar')
            self.teach_move(dance_interactive='sprinkler')
            self.say("Now let's just have some fun and dance together!")
            self.dance_together()
            self.say(random.choice(self.speech_options.end_message))

    def main(self):
        # Start the GUI in a separate thread
        gui_thread = threading.Thread(target=self.gui_stop, daemon=True)
        gui_thread.start()

        # Run main program
        self.introduction()
        self.scenario()
  
if __name__ == "__main__":
    nao = NaoDanceTutor()
    nao.main()


