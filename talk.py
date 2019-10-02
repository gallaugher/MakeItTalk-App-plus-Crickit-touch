# talk.py
# once running, you can test with the shell commands:
# To start the robot:
# mosquitto_pub -h talkpi.local -t "talkpi/talk" -m "yes.mp3"

import paho.mqtt.client as mqtt
import pygame
import time
from adafruit_crickit import crickit

clientName = "talk"
serverAddress = "talkpi" # problems connecting? try <your server name>.local
mqttClient = mqtt.Client(clientName)
fileLocation = "/home/pi/sounds/"
leftLocation = "/home/pi/lefthand/"
rightLocation = "/home/pi/lefthand/"
leftSound = 0
rightSound = 0
leftSounds = ["seeking_professor_g_you_are.mp3",
              "welcome_you_are_happy_to_see_you.mp3",
              "awesomeness_you_bring_yes.mp3",
              "trust_in_the_one_who_is_bald_and_wears_a_beard_wise_he_is.mp3",
              "wish_you_well_i_do_may_the_force_be_with_you.mp3"
              ]
rightSounds = ["hungry_are_you_skittles_you_may_have.mp3",
               "bc_we_are.mp3",
               "taught_baldwin_to_fly_i_have.mp3",
               "wonder_i_am_a_person_for_others_are_you.mp3"]

# init pygame.mixer, which plays audio in our program.
# Test, Yoda should say Yes each time he's started up
# You should change this line so that it contains a file on
# your Raspberry Pi.
pygame.mixer.init()
pygame.mixer.music.load(fileLocation + "yes.mp3") # assumes you have a file with this name in a /home/pi/sounds directory
speakerVolume = "0.5" # initially sets speaker at 50%
pygame.mixer.music.set_volume(float(speakerVolume))
pygame.mixer.music.play()

def connectionStatus(client, userdata, flags, rc):
    print("subscribing")
    mqttClient.subscribe("talkpi/talk")
    print("subscribed")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    # Feel free to remove the print, but confirmation in the terminal is nice.
    print("^^^ payload message = ", message)
    if message.startswith("vol-"):
        # Mac slider sends messages as a String "vol-#.#" where #.# is from 0.0 to 1.0.
        message = message.strip("vol-")
        speakerVolume = float(message)
        pygame.mixer.music.set_volume(speakerVolume)
    else:
        pygame.mixer.music.load(fileLocation + message)
        pygame.mixer.music.play()
        time.sleep(1.0) # wait 1 second between plays.

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
mqttClient.connect(serverAddress)
# mqttClient.loop_forever()

while True:
    mqttClient.loop()
    if crickit.touch_1.value:
        print("Touched Cap Touch Pad 1")
        pygame.mixer.music.load(fileLocation + leftSounds[leftSound])
        pygame.mixer.music.play()
        leftSound = leftSound + 1
        if leftSound == len(leftSounds):
             leftSound = 0
    if crickit.touch_3.value:
        print("Touched Cap Touch Pad 3")
        pygame.mixer.music.load(fileLocation + rightSounds[rightSound])
        pygame.mixer.music.play()
        rightSound = rightSound + 1
        if rightSound == len(rightSounds):
            rightSound = 0
    time.sleep(0.25) # wait a quarter second.

