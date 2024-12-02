class SpeechAlternatives:
    def __init__(self):
        self.intro = [
                            "Hi there! What's your name?",
                            "Hello! May I ask your name?",
                            "Hey! What's your name?",
                            "Hello, what's your name?",
                            "Hi! Can you tell me your name?",
                            "Hey there! What's your name?",
                            "Hi! Who are you?",
                            "Hello! Could you share your name?",
                            "Hi! What should I call you?",
                            "Greetings! What's your name?"
                        ]
        self.not_understood_name = [
                            "I'm sorry, I didn't get your name. Please say it again.",
                            "Sorry, I didn't catch your name. Could you repeat it?",
                            "Apologies, I missed your name. Would you mind saying it again?",
                            "Sorry, I didn't hear your name. Can you tell me again?",
                            "Excuse me, I didn't quite catch your name. Could you repeat it?",
                            "I'm sorry, I didn't quite get your name. Could you say it once more?",
                            "Sorry, I missed your name. Could you please say it again?",
                            "I apologize, I didn't understand your name. Can you say it again?",
                            "Excuse me, I didn't hear your name clearly. Can you repeat it?",
                            "Sorry about that, could you please say your name again?"
                        ]
        self.greetings = [
                            f"Hi {name}! My name is Nao, I am here to teach you some cool moves, but most importantly: to have fun together!",
                            f"Hey {name}! I'm Nao, and I'm excited to teach you some awesome moves and, more importantly, have fun together!",
                            f"Hello {name}! I'm Nao, and I'm here to show you some cool moves while we have a great time together!",
                            f"Hi {name}! I'm Nao, ready to teach you some fun moves and, most importantly, enjoy ourselves!",
                            f"Hey {name}! Nao here! I'm excited to teach you some fun moves, but the best part is having fun together!",
                            f"Hello {name}! My name's Nao, and I'm here to help you learn some cool moves and, of course, have fun!",
                            f"Hi {name}! I'm Nao, and I'm looking forward to teaching you some awesome moves and having a blast together!",
                            f"Hey {name}! It's Nao! Let's learn some cool moves and, most importantly, have a great time together!",
                            f"Hello {name}! My name is Nao, and I'm here to teach you some cool moves while we enjoy ourselves!",
                            f"Hi {name}! I'm Nao, ready to show you some great moves, but the most important thing is having fun together!"
                        ]
        self.intro_options = [
                            "First off, you can choose whether you want to learn a dancemove, or to just dance together. What would you prefer?",
                            "To start, you can decide if you'd like to learn a dance move or just dance together. What do you prefer?",
                            "First, you can pick whether you'd like to learn a dancemove or simply dance together. What do you prefer?",
                            "Let's begin! You can choose between learning a dancemove or just dancing together. Which one would you like?",
                            "To start things off, you can decide if you want to learn a dancemove or just enjoy dancing together. What would you prefer?",
                            "First up, you can choose whether you'd like to learn a new dancemove or just dance together. What sounds better to you?",
                            "Let's kick things off! Would you like to learn a dancemove or just dance together? What would you prefer?",
                            "To get started, you can choose to learn a dancemove or just dance with me. What would you prefer?",
                            "First, you get to decide whether you'd like to learn a dancemove or simply dance together. What's your choice?",
                            "Let's start! You can pick whether to learn a dancemove or just enjoy dancing together. What do you prefer?"
                        ]
        self.scenario_options = [
                            "Would you like to learn another move, dance together or stop?",
                            "Do you want to learn another move, dance together, or quit?",
                            "Would you prefer to learn another move, keep dancing, or stop for now?",
                            "What would you like to do next? Learn another move, dance together, or stop?",
                            "Would you like to try another move, dance together some more, or stop?",
                            "Do you want to continue with another move, dance together, or stop for the moment?",
                            "What's next? Do you want to learn another move, dance together, or stop?",
                            "Would you like to practice another move, keep dancing, or stop here?",
                            "Do you want to learn another move, enjoy more dancing, or stop now?",
                            "What's your choice? Learn another move, dance together, or stop?"
                        ]
        self.end_message = [
                            "Alright, thanks a lot for joining, I had a lot of fun! I hope to see you again!",
                            "Thanks so much for joining! I had a great time and hope to see you again soon!",
                            "It was awesome having you here, thanks for joining! I hope we can do it again sometime!",
                            "Thank you so much for joining! I had a blast and look forward to seeing you again!",
                            "Thanks for being here, I had so much fun! Hope to see you again soon!",
                            "I really appreciate you joining! I had a fantastic time and hope we meet again!",
                            "Thank you for joining! I had a wonderful time and can't wait to see you again!",
                            "It was great having you here! Thanks for joining, and I hope to see you again soon!",
                            "Thanks a lot for joining! I had an amazing time, and I hope we can do it again sometime!",
                            "I had a lot of fun, thanks for joining! I look forward to seeing you again!"
                        ]
        self.scenario_misunderstood = [
                            "I'm sorry, I didn't understand that. Could you please say again if you would like to dance together or learn a move?",
                            "Sorry, I didn't quite catch that. Could you repeat if you want to dance together or learn a move?",
                            "Apologies, I didn't understand. Could you please tell me again if you'd like to dance together or learn a move?",
                            "I'm sorry, I didn't quite get that. Can you repeat whether you want to dance together or learn a move?",
                            "Sorry, I didn't understand. Could you say again if you'd prefer to dance together or learn a move?",
                            "Sorry, I didn't catch that. Could you please clarify if you want to dance together or learn a move?",
                            "I'm sorry, I missed that. Can you repeat whether you want to learn a move or dance together?",
                            "I didn't quite understand. Could you please say again if you'd like to learn a move or dance together?",
                            "Apologies, I didn't quite hear that. Can you clarify if you want to dance together or learn a move?",
                            "Sorry, I didn't get that. Can you please repeat if you'd like to learn a move or dance together?"
                        ]
        self.dance_together_intro = [
                            "Alrighty! Are you ready?",
                            "Okay! Are you all set?",
                            "Great! Are you ready to go?",
                            "Alright! Are you prepared?",
                            "Let's get started! Are you ready?",
                            "Okay then! Are you ready to begin?",
                            "Let's do this! Are you ready?",
                            "Alright! Are you good to go?",
                            "Great! Are you ready to start?",
                            "Okay! Are you set to go?"
                        ]
        self.dance_together_start = [
                            "Here we go!",
                            "Let's do this!",
                            "And we're off!",
                            "Let's get started!",
                            "Here we are!",
                            "Let's get moving!",
                            "Time to start!",
                            "Off we go!",
                            "Let's get going!",
                            "Here it is!"
                        ]
        self.dance_together_feedback = [
                            f"Wow! I saw that you did a perfect {dance}",
                            f"Impressive! You nailed that {dance}!",
                            f"Nice! That was a flawless {dance}!",
                            f"Great job! You did a perfect {dance}!",
                            f"Wow, that was an amazing {dance}!",
                            f"Awesome! You pulled off that {dance} perfectly!",
                            f"That was perfect! I saw you do a great {dance}!",
                            f"Impressive! Your {dance} was spot on!",
                            f"Fantastic! You executed that {dance} flawlessly!",
                            f"Great work! That {dance} was perfect!"
                        ]
        self.dance_together_end = [
                            "Wow, that was fun! I'm a bit tired now to be honest.",
                            "That was awesome! I'm feeling a little tired now, to be honest.",
                            "What a great time! I'm starting to feel a bit tired now.",
                            "That was so much fun! I'm a little tired now, to be honest.",
                            "Wow, that was amazing! I'm a bit worn out now, if I'm being honest.",
                            "That was a blast! I'm starting to feel a little tired now.",
                            "I had so much fun! I'm a bit tired now, though.",
                            "What a great session! I'm feeling a little tired now, to be honest.",
                            "That was really fun! I'm a bit exhausted now, to be honest.",
                            "That was fantastic! I'm feeling a little tired now, to tell you the truth."
                        ]
        self.desired_move = [
                            "Alright! Would you like to learn how to dab, a sprinkler or an air guitar?",
                            "Okay! Do you want to learn the dab, the sprinkler, or air guitar?",
                            "Great! Would you like to try the dab, the sprinkler, or air guitar?",
                            "Alright, which one would you like to learn: the dab, a sprinkler, or air guitar?",
                            "Hey! Do you want to learn how to do the dab, a sprinkler, or air guitar?",
                            "Ready? Would you like to learn the dab, a sprinkler, or air guitar?",
                            "Alright! What do you prefer to learn: the dab, sprinkler, or air guitar?",
                            "What would you like to learn today? The dab, a sprinkler, or air guitar?",
                            "Okay, let's get started! Do you want to learn the dab, the sprinkler, or air guitar?",
                            "What do you want to learn: the dab, a sprinkler, or air guitar?"
                        ]
        self.desired_move_misunderstand = [
                            "Sorry, I didn't understand. Would you like to learn how to dab, a sprinkler or an air guitar?",
                            "Apologies, I didn't quite catch that. Would you like to learn the dab, a sprinkler, or air guitar?",
                            "Sorry, I missed that. Would you like to learn how to do the dab, the sprinkler, or air guitar?",
                            "I'm sorry, I didn't understand. Would you prefer to learn the dab, a sprinkler, or air guitar?",
                            "Sorry, I didn't get that. Would you like to try the dab, a sprinkler, or air guitar?",
                            "I didn't quite understand. Would you like to learn the dab, a sprinkler, or air guitar?",
                            "Sorry, I didn't catch that. Would you like to try the dab, a sprinkler, or air guitar?",
                            "Apologies, I didn't quite hear that. Would you like to learn the dab, sprinkler, or air guitar?",
                            "I'm sorry, I didn't understand. Can you clarify if you'd like to learn the dab, a sprinkler, or air guitar?",
                            "Sorry, I didn't get that. Would you like to learn the dab, a sprinkler, or air guitar instead?"
                        ]
        self.teach_intro = [
                            f"Sure thing! Let me teach you how to do a {dance}! Watch how I do it.",
                            f"Alright! Let me show you how to do a {dance}. Pay attention to how I do it.",
                            f"Of course! Let me teach you the {dance}. Watch closely as I demonstrate it.",
                            f"Got it! Let me show you how to do a {dance}. Follow along with how I do it.",
                            f"Absolutely! Let me teach you the {dance}. Keep an eye on how I perform it.",
                            f"Sure! Let me show you how to do a {dance}. Watch me carefully!",
                            f"Definitely! I'll teach you the {dance}. Take a look at how I do it.",
                            f"Alright! I'll show you how to do a {dance}. Watch how I move.",
                            f"Sounds good! Let me teach you how to do a {dance}. Watch me first!",
                            f"Absolutely! Let me demonstrate the {dance}. Watch closely and learn!"
                        ]
        self.teach_start = [
                            "Now you try to do it!",
                            "Your turn to give it a shot!",
                            "Now it's your turn to try!",
                            "Go ahead, try it yourself!",
                            "Now you take a crack at it!",
                            "Alright, give it a go yourself!",
                            "Your turn! Show me what you've got!",
                            "Now it's time for you to try!",
                            "Give it a try now, it's your turn!",
                            "Okay, now try doing it!"
                        ]
        self.positive_feedback = [
                            "Amazing! Let's try it again!",
                            "Fantastic! Let's give it another go!",
                            "Awesome! Let's try that once more!",
                            "Great job! Let's do it again!",
                            "Incredible! Let's try it again!",
                            "Wonderful! Let's give it another shot!",
                            "That was awesome! Let's do it again!",
                            "Impressive! Let's try it one more time!",
                            "Excellent! Let's give it another try!",
                            "You're doing great! Let's try it again!"
                        ]
        self.negative_feedback = [
                            f"Nice try! But I think you can do it better. I'll show you again. Pay attention to my {worst_error_bodypart}",
                            f"Good attempt! But I think you can improve. Let me show you again. Watch my {worst_error_bodypart}.",
                            f"Nice effort! I know you can do better. Let me demonstrate again. Focus on my {worst_error_bodypart}.",
                            f"Good try, but I think you can do it better. Let me show you one more time. Pay attention to my {worst_error_bodypart}.",
                            f"Nice attempt! But I believe you can do it better. Let me show you again. Look closely at my {worst_error_bodypart}.",
                            f"Great try! But I think there's room for improvement. Let me show you again. Watch my {worst_error_bodypart}.",
                            f"Not bad, but I know you can do it even better. Let me demonstrate once more. Pay attention to my {worst_error_bodypart}.",
                            f"You're getting there! But I think you can improve. Let me show you again. Watch my {worst_error_bodypart} carefully.",
                            f"Nice work, but I think you can perfect it. Let me demonstrate again. Pay attention to my {worst_error_bodypart}.",
                            f"Good job, but I know you can do it even better. Let me show you again. Focus on my {worst_error_bodypart} this time."
                        ]
        self.teach_resume = [
                            "And now you again.",
                            "Your turn again!",
                            "Now it's your turn once more.",
                            "Now you go again!",
                            "It's time for you again!",
                            "Your turn again, let's see it!",
                            "Now it's time for you to try again.",
                            "And now, back to you!",
                            "Alright, now it's your turn again!",
                            "Now let's see you do it again!"
                        ]
        self.teach_end = [
                            f"Good job! You've learned how to do a {dance}!",
                            f"Great work! You've mastered the {dance}!",
                            f"Awesome! You've learned how to do the {dance}!",
                            f"Well done! You now know how to do a {dance}!",
                            f"Nice job! You've nailed the {dance}!",
                            f"Fantastic! You've learned the {dance} perfectly!",
                            f"Excellent! You've got the {dance} down!",
                            f"Bravo! You've successfully learned the {dance}!",
                            f"Awesome job! You've learned how to do the {dance}!",
                            f"Perfect! You've mastered the {dance}!"
                        ]
        self.teach_loop_check = [
                            "Do you still want to continue, or do you want to do something else?",
                            "Would you like to keep going, or try something different?",
                            "Do you want to continue, or would you prefer to do something else?",
                            "Are you ready to keep going, or would you like to switch it up?",
                            "Would you like to carry on, or do something else instead?",
                            "Do you want to keep going, or try something else?",
                            "Should we continue, or would you prefer to do something else?",
                            "Would you like to keep going, or would you prefer to change things up?",
                            "Do you still want to continue, or is there something else you'd like to do?",
                            "Do you want to keep going, or try a different activity?"
                        ]
        self.left_message = [
                            "It seems like you left. I would love it if you would come back for some dancing.",
                            "Looks like you've left. I'd really love it if you came back for some dancing!",
                            "It seems you've gone. I'd be so happy if you came back for some more dancing.",
                            "It looks like you've left. I'd love for you to return and join in the dancing!",
                            "It seems like you stepped away. I'd love it if you came back and danced with me.",
                            "Looks like you've gone. I'd really enjoy it if you came back and danced!",
                            "It seems like you left. I'd love for you to come back and dance some more.",
                            "It looks like you've left. Come back and let's keep dancing!",
                            "I think you've left. I'd love for you to come back and join in the dance!",
                            "It seems like you've gone. Come back for some more dancing – I'd love that!"
                        ]
        self.welcome_back = [
                            "Welcome back! Let's continue.",
                            "Glad to have you back! Let's keep going.",
                            "Welcome back! Ready to continue?",
                            "Hey, welcome back! Let's get back to it.",
                            "Great to see you again! Let's continue.",
                            "Welcome back! Let's carry on.",
                            "Nice to have you back! Let's keep it going.",
                            "Welcome back! Ready to pick up where we left off?",
                            "Hey, glad you're back! Let's continue from where we stopped.",
                            "Welcome back! Let's get back to dancing."
                        ]
        self.cry = [
                            "I guess you're not coming back, I will go cry now.",
                            "Looks like you're not coming back, guess I'll cry now.",
                            "I suppose you're not returning, time for me to cry.",
                            "Seems like you're not coming back, I guess I'll go cry.",
                            "I guess you're not coming back, so I'll just cry now.",
                            "Looks like you're not returning, guess I'm going to cry.",
                            "Seems like you're not coming back, guess I'll cry now.",
                            "I guess you're not coming back, guess I'll cry by myself.",
                            "I suppose you're not coming back, so I'll go cry now.",
                            "It seems like you're not coming back, time for me to cry."
                        ]






















