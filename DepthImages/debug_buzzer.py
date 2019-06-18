class debug_haptic():

    def __init__(self):
        print("Haptics are fired up!")

    def playEffect(self, effect):
        if effect == 12:
            print("Beep! Beep! Beep!")
        elif effect == 10:
            print("Beep! Beep!")
        elif effect == 1:
            print("Beep!")
        else:
            print("Error: Invalid effect code of " + str(effect))
