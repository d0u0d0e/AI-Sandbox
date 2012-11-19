# Your AI for CTF must inherit from the base Commander class.  See how this is
# implemented by looking at the commander.py in the ./api/ folder.
from api import Commander

# The commander can send 'Commands' to individual bots.  These are listed and
# documented in commands.py from the ./api/ folder also.
from api import commands

# The maps for CTF are layed out along the X and Z axis in space, but can be
# effectively be considered 2D.
from api import Vector2


import math
import random as rand

class PlaceholderCommander(Commander):
    """
    Rename and modify this class to create your own commander and add mycmd.Placeholder
    to the execution command you use to run the competition.
    """

    def initialize(self):
        """Use this function to setup your bot before the game starts."""
        self.verbose = True    # display the command descriptions next to the bot labels
        self.numbots = len(self.game.bots_alive)
        self.timer = 0
        self.timerspan = 30

        print 'width: ' + str(self.level.width)
        print 'height: ' + str(self.level.height)        

    def tick(self):
        """Override this function for your own bots.  Here you can access all the information in self.game,
        which includes game information, and self.level which includes information about the level."""

        # Give the bot a random move location every self.timerspan timer ticks
        if self.timer == 0:
            i = 0
            for bot in self.game.bots_alive:
                randompos = False
                while not randompos:
                    randompos = Vector2(rand.random() * self.level.width, rand.random() * self.level.height)
                    randompos = self.level.findNearestFreePosition(randompos)
                    
                self.issue(commands.Attack,
                           bot,
                           randompos,
                           self.look(i / float(self.numbots)),
                           description = "[" + str(int(randompos.x)) + ", " + str(int(randompos.y)) + "]")
                i = i + 1

        self.timer = (self.timer + 1) % self.timerspan
           

        
        
        """
        # for all bots which aren't currently doing anything
        for bot in self.game.bots_available:
            if bot.flag:
                # if a bot has the flag run to the scoring location
                flagScoreLocation = self.game.team.flagScoreLocation
                self.issue(commands.Charge, bot, flagScoreLocation, description = 'Run to my flag')
            else:
                # otherwise run to where the flag is
                enemyFlag = self.game.enemyTeam.flag.position
                self.issue(commands.Charge, bot, enemyFlag, description = 'Run to enemy flag')
        """

    def shutdown(self):
        """Use this function to teardown your bot after the game is over, or perform an
        analysis of the data accumulated during the game."""

        pass

    def look(self, f):
        """ Retrun a Vector2 that points in the direction of 2pi * f """

        return_vec = Vector2()
        angle = 2 * math.pi * f
        
        return_vec.x = (self.level.width - 1) * abs(math.sin(angle))
        return_vec.y = (self.level.height - 1) * abs(math.cos(angle))

        return return_vec


        
