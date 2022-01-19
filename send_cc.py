import sys
import mido
from time import sleep

for port in mido.get_output_names():
    if port[:9]=="UNO Synth":
        outport = mido.open_output(port)
        print("Using Output:", port)
        break


if outport == None:
    sys.exit("Unable to find UNO Synth")

print("sending on CC", sys.argv[1])
msg = mido.Message("control_change", channel=0, control=int(sys.argv[1]), value=int(sys.argv[2]))
print(msg)
outport.send(msg)
