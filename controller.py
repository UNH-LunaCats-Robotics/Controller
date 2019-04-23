from enum import Enum

import pygame
import requests
from time import sleep

raspberryIPLocation = "http://10.0.10.10:5000/cmd/"

class Move(Enum):
    FORWARD = "{'c':0}"
    BACK    = "{'c':1}"
    LEFT    = "{'c':2}"
    RIGHT   = "{'c':3}"
    STOP    = "{'c':4}"
    RAISE_F = "{'c':10}"
    LOWER_F = "{'c':11}"


def sendCommand(movement = Move.STOP):
    global raspberryIPLocation
    requests.get(raspberryIPLocation + movement.value)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

joystickInputValue = 0.5

prevMove = Move.STOP

def getJoystickCommand( axis, value ):
    global joystickInputValue
    #print("axis: ", axis, "\tvalue: ", axis)
    if axis == 1:
       #joystick reads forward command
       if  value < 0 and value < -joystickInputValue:
           return Move.FORWARD
        #joystick reads back command
       elif value > 0 and value > joystickInputValue:
           return Move.BACK
    elif axis == 2:
        if value < 0 and value < -joystickInputValue:
            return Move.LEFT
        elif value > 0 and value > joystickInputValue:
            return Move.RIGHT
    return Move.STOP

def printJoystickMove(move):
    if move == Move.STOP:
        print("STOP")
    elif move == Move.LEFT:
        print("LEFT")
    elif move == Move.RIGHT:
        print("RIGHT")
    elif move == Move.FORWARD:
        print("FORWARD")
    elif move == Move.BACK:
        print("BACK")
    elif move == Move.RAISE_F:
        print("RAISE FRAME")
    elif move == Move.LOWER_F:
        print("LOWER FRAME")
    else:
        print("Incorrect Value Given")


def runRobotJoystickCommands(joystick):
    global prevMove
    buttons = joystick.get_numbuttons()
    axes = joystick.get_numaxes()
    move = Move.STOP

    for i in range(axes):
        axis = joystick.get_axis(i)

        move = getJoystickCommand(i, axis)
        if move != move.STOP:
            break
        #printJoystickMove(move)

    for i in range(buttons):
        button = joystick.get_button(i)
        if i == 5 and button:
            move = Move.LOWER_F
        if i == 7 and button:
            move = Move.RAISE_F

    if True: #move != prevMove:

        print("prevMove: ", prevMove, "currentMove: ", move)
        try:
            sendCommand(move)
            #sleep(1.5)
        except Exception:
            print("Cannot send command!!!!!")

        prevMove = move


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()


# Loop until the user clicks the close button.
done = False

#prevAxis = -1

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        runRobotJoystickCommands(joystick)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
