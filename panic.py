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


#This sends commands that it's given to the raspberry pi, and then records it
def sendCommand(movement = Move.STOP):
    global raspberryIPLocation, previousMove, speed
    requests.get(raspberryIPLocation + movement.value,timeout=1) 


while True:
    cmd = input("Cmd:")
    if(cmd == "w"):
        sendCommand(Move.FORWARD)
        print("Works!")
    if(cmd == "s"):
        sendCommand(Move.BACK)
        print("Works!")
    if(cmd == "a"):
        sendCommand(Move.LEFT)
        print("Works!")
    if(cmd == "d"):
        sendCommand(Move.RIGHT)
        print("Works!")
    if(cmd == "d"):
        sendCommand(Move.RIGHT)
        print("Works!")
    if(cmd == "z"):
        sendCommand(Move.STOP)
        print("Works!")