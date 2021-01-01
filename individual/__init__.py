class Individual():
    def __init__(self, gender, iq, age, can_have_baby):
        """Initialize instance variables."""
        self.gender = gender
        self.iq = iq
        self.age = age
        # Whether the individual has a spouse or not
        self.couple = None
        # Whether the individual has a child (Can only have one child)
        self.child = False
        # Variable used for sterilization
        self.can_have_baby = can_have_baby
    
    def marry(self, opponent):
        self.couple = opponent

    def addChild(self, child):
        self.child.append(child)
        