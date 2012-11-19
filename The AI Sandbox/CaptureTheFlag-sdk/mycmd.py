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

        # Set up the distribution of defenders and attackers
        self.defenders = 2
        self.attackers = len(self.game.bots_alive) - self.defenders # Rest are attackers
        
        # Set up the Bot Action Queue.
        self.BAC = {}
        
        # Add the first command for the defenders to the BAC
        for i in range(self.defenders):
            bot = self.game.bots_alive[i]
            self.BAC[bot] = []
            
            self.issue(commands.Move, bot, self.game.team.flag.position, description ='MOVE') #self.BAC[bot] = [(commands.Move, bot, self.game.team.flag.position, 'MOVE')]
            self.issue(commands.Defend, bot, self.game.enemyTeam.flag.position, description = 'DFND') #self.BAC[bot].append((commands.Defend, bot, self.game.enemyTeam.flag.position, 'DFND'))
            
        # Add the first command for the attackers to the BAC
        for i in range(self.defenders, self.attackers + self.defenders):
            bot = self.game.bots_alive[i]
            self.BAC[bot] = [(commands.Attack, bot, self.game.enemyTeam.flag.position, 'ATCK')]


        print 'width: ' + str(self.level.width)
        print 'height: ' + str(self.level.height)

    def tick(self):
        """Override this function for your own bots.  Here you can access all the information in self.game,
        which includes game information, and self.level which includes information about the level."""

        """
        # Give the bot a random attack location every self.timerspan ticks
        if self.timer == 0:
            for bot in self.game.bots_alive:

                # Generate a random valid position on the map.
                randompos = False
                while not randompos:
                    randompos = Vector2(rand.random() * self.level.width, rand.random() * self.level.height)
                    randompos = self.level.findNearestFreePosition(randompos)

                # Attack at the random position.
                self.issue(commands.Attack,
                           bot,
                           randompos,
                           description = "[" + str(int(randompos.x)) + ", " + str(int(randompos.y)) + "]")

        self.timer = (self.timer + 1) % self.timerspan # Increment the timer.
        """

        for bot in self.game.bots_available:
            if len(self.BAC[bot]) > 0:
                cmd = self.BAC[bot].pop(0)
                
                self.issue(cmd[0], cmd[1], cmd[2], description = cmd[3])


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
