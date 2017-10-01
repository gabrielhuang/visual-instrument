import numpy as np
import cv2
import mido
from mido import Message
import pickle

with open('detections.pkl', 'rb') as fp:
    detections = pickle.load(fp)

NOTES = {
    'kick':  36,
    'snare':  40,
    'hat':  44,
}

class Player(object):
    def __init__(self, notes, sustain=3):
        self.notes = notes
        self.sustain = sustain
        self.last_played = {note: None for note in notes}
        self.clear()

    def clear(self):
        for note, note_val in self.notes.items():
            outport.send(Message('note_off', note=note_val))

    def play(self, instrument, idx):
        note = self.notes[instrument]
        self.last_played[note] = idx
        outport.send(Message('note_on', note=note))

    def mute_old(self, idx):
        for note, last_played in self.last_played.items():
            if last_played is not None and idx > last_played + self.sustain:
                outport.send(Message('note_off', note=note))
    
### MAIN ###
list_ports = mido.get_output_names()
print list_ports
port_id = 1
outport = mido.open_output(list_ports[port_id])

continue_ = True
while continue_:
    cap = cv2.VideoCapture('result.avi')
    #cap = cv2.VideoCapture('impacts.avi')

    idx = 0
    player = Player(NOTES)
    while True:
        r, frame = cap.read()
        for instrument in detections:
            if idx in detections[instrument]:
                player.play(instrument, idx)
        if not r:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ' ':
            continue_ = False
            break

        player.mute_old(idx)
        idx += 1
    print 'looping'
