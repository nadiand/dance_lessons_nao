import stk.python27bridge
import stk.events
import stk.services
import dances

class Python3NaoExample:
    def __init__(self):
        # Bridge
        self.python27bridge = stk.python27bridge.Python27Bridge()
        self.events = stk.events.EventHelper(self.python27bridge)
        self.s = stk.services.ServiceCache(self.python27bridge)
        # Test speech
        self.s.ALTextToSpeech.say("Luuk has beautiful eyes")
        # Import from dances file
        Dances = dances.Dances()

        dance = Dances.air_guitar(multiplier=0.5)
        self.s.ALMotion.angleInterpolationBezier(dance[0], dance[1], dance[2])

        dance = Dances.dance_move()
        self.s.ALMotion.angleInterpolationBezier(dance[0], dance[1], dance[2])

    
if __name__ == "__main__":
    Python3NaoExample()
