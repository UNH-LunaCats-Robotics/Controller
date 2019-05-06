from enum import Enum

import pygame
import requests
from time import sleep


raspberryIPLocation = "http://10.0.10.10:5000/cmd/"

#This is every defined movement command for the robot, to add new commands you need to simply expand this list and add code for the axis check
class Move(Enum):
    FORWARD = "{\"c\":0}"
    BACK    = "{\"c\":1}"
    LEFT    = "{\"c\":2}"
    RIGHT   = "{\"c\":3}"
    STOP    = "{\"c\":4}"
    RAISE_F = "{\"c\":10}"
    LOWER_F = "{\"c\":11}"
    INCREASE_SPEED = "{\"c\":12}"
    DECREASE_SPEED = "{\"c\":13}"
    CONVEYOR_COLLECT = "{\"c\":14}"
    CONVEYOR_DUMP = "{\"c\":15}"
    TURN_AUGUR_CLOCKWISE = "{\"c\":16}"
    TURN_AUGUR_COUNTER_CLOCKWISE = "{\"c\":17}"
    BALL_SCREW_UP = "{\"c\":18}"
    BALL_SCREW_DN = "{\"c\":19}"

previousMove = Move.STOP
speed = 10

#This sends commands that it's given to the raspberry pi, and then records it
def sendCommand(movement = Move.STOP):
    global raspberryIPLocation, previousMove, speed
    try:
        response = requests.get(raspberryIPLocation + movement.value,timeout=1) 
        print("Sent message:"+movement.value )
        if movement.value == Move.INCREASE_SPEED:
            speed += 5;
        if movement.value == Move.DECREASE_SPEED:
            speed -= 5;

        previousMove = movement
    except:
        print("error sending message:" + movement.value)
        previousMove = None
        sleep(3)
    

#This checks the commands to send to the raspberry pi to make sure you're not sending one you already sent. if you aren't, it sends the command
def checkCommand(movement = Move.STOP):
    global previousMove
    if movement != previousMove:
        sendCommand(movement)
        print("Sending:"+str(movement))

import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

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
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    

    moveCmd = Move.STOP

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )

            if i == 1 and axis < -0.5:
                moveCmd = Move.FORWARD
            if i == 1 and axis > 0.5:
                moveCmd = Move.BACK
            if i == 2 and axis > 0.5:
                moveCmd = Move.LEFT
            if i == 2 and axis < -0.5:
                moveCmd = Move.RIGHT
        
        

        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
            if i == 7 and button > 0.5:
                moveCmd = Move.RAISE_F
            if i == 5 and button > 0.5:
                moveCmd = Move.LOWER_F
            if i == 6 and button > 0.5:
                moveCmd = Move.CONVEYOR_COLLECT
            if i == 4 and button > 0.5:
                moveCmd = Move.CONVEYOR_DUMP
            if i == 0 and button > 0.5:
                moveCmd = Move.BALL_SCREW_DN
            if i == 1 and button > 0.5:
                moveCmd = Move.BALL_SCREW_UP
            if i == 2 and button > 0.5:
                moveCmd = Move.TURN_AUGUR_CLOCKWISE
            if i == 3 and button > 0.5:
                moveCmd = Move.TURN_AUGUR_COUNTER_CLOCKWISE
        
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
            if hat[1] > 0.5:
                moveCmd = Move.INCREASE_SPEED
            if hat[1] < -0.5:
                moveCmd = Move.DECREASE_SPEED
        textPrint.unindent()
        textPrint.print(screen, "Speed: {}".format(speed) )

        textPrint.unindent()
       

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    #Send the Request
    checkCommand(moveCmd)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
