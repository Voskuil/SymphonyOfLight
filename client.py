import pygame
import pygame.midi
from pygame.locals import *
from time import sleep
import time
import socket
import sys

pygame.init()

pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input( input_id )

HOST, PORT = "pbridge.adm.cs.cmu.edu",9999
data = "0"


pygame.display.set_caption("midi test")
screen = pygame.display.set_mode((400, 300), RESIZABLE, 32)
port = pygame.midi.get_default_output_id()
print ("using output_id :%s:" % port)
midi_out = pygame.midi.Output(port, 0)
midi_out.set_instrument(1)
print "starting"

going = True
while going:

        events = event_get()
        for e in events:
                if e.type in [QUIT]:
                        going = False

        if i.poll():
                midi_events = i.read(10)
                midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
                for m_e in midi_evs:
                        event_post( m_e )
                if midi_events[0][0][0] == 144:
                        midi_out.note_on(midi_events[0][0][1],min(midi_events[0][0][2]+30,127)) # 74 is middle C, 127 is "how loud" - max is 127
                print "full midi_events " + str(midi_events)
                color = midi_events[0][0][1] - 36
                intensity = midi_events[0][0][2] + 20
                hit = (midi_events[0][0][0]-128) and 1
                data = str(hit) + "*" + str(color) + "*" + str(intensity)
                print data
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.connect((HOST,PORT))
                sock.sendall(data+"\n")
                #data = str(int(data)+1)
                print "RECEIVED: {}".format(sock.recv(1024))
                sock.close()
                #Convert this data into a string
                #Send it to server
                #???
                #Profit

print "exit button clicked."
i.close()
pygame.midi.quit()
pygame.quit()
exit()
