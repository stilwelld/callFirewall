#!/usr/bin/env python3

# RASPBERRY PI VERSION

import time
import socket
import select
from gtts import gTTS
import sys
  
# This module is imported so that we can 
# play the converted audio
import os

timeout = 5000
count = 0
# Language in which you want to convert
language = 'en'

UDP_IP = "0.0.0.0"
UDP_PORT = 33000
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

while True:

  # use select to see if data is waiting
  ready = select.select([sock], [], [], 0.4)
 
  if ready[0]: 
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    msg = data.decode('ascii')
    myobj = gTTS(text=msg, lang=language, slow=False)
  
    # Saving the converted audio in a mp3 file named
    # announce 
    myobj.save("/tmp/announce.mp3")
  
    # Playing the converted file
    os.system("mpg321 -q -g 10 /tmp/announce.mp3")
    #
