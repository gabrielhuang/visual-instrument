import mido
import time
from mido import Message

#mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')

bpm = 110.
ts = 60./bpm
port_id = [6,7]
outport = []

list_ports = mido.get_output_names()
print list_ports
for i in port_id:
    print list_ports[i]
    outport.append(mido.open_output(list_ports[i]))
while True:
    try:
        outport[0].send(Message('note_on', note=28))
        outport[1].send(Message('note_on', note=28))
        time.sleep(4*ts)
        outport[0].send(Message('note_off', note=28))
        outport[1].send(Message('note_off', note=28))
        outport[0].send(Message('note_on', note=31))
        outport[1].send(Message('note_on', note=31))
        time.sleep(4*ts)
        outport[0].send(Message('note_off', note=31))
        outport[1].send(Message('note_off', note=31))
        outport[0].send(Message('note_on', note=35))
        outport[1].send(Message('note_on', note=35))
        time.sleep(4*ts)
        outport[0].send(Message('note_off', note=35))
        outport[1].send(Message('note_off', note=35))
        outport[0].send(Message('note_on', note=37))
        outport[1].send(Message('note_on', note=37))
        time.sleep(4*ts)
        outport[0].send(Message('note_off', note=37))
        outport[1].send(Message('note_off', note=37))
    except KeyboardInterrupt:
        for i in range(0,127):
            outport[0].send(Message('note_off', note=i))
            outport[1].send(Message('note_off', note=i))

        raise
