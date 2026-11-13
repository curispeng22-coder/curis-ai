"""Original deterministic synthesis fixtures, not vocals or Provider-generated music."""
import math, wave, struct, json
from pathlib import Path
root=Path(__file__).parent
rate=22050
for variant,tempo in [('a',92),('b',104),('c',100)]:
    samples=[]
    notes=[220,261.6256,329.6276,293.6648,220,392,329.6276,261.6256]
    for i in range(rate*32):
        t=i/rate; beat=t*tempo/60; frac=beat%1
        chord=int(beat//4)%4; base=[110,130.8128,87.3071,97.9989][chord]
        pad=sum(math.sin(2*math.pi*base*r*t) for r in [1,1.5,2.5])*0.04
        kick=math.sin(2*math.pi*(44*t+2*(1-math.exp(-frac*25))))*math.exp(-frac*15)*0.22
        eighth=(beat*2)%1
        melody=math.sin(2*math.pi*notes[int(beat*2)%8]*t)*math.exp(-eighth*(5 if variant=='a' else 9))*0.10
        hook=1 if t>= (12 if variant=='a' else 8) else .35
        hat=math.sin(2*math.pi*6401*t)*math.exp(-eighth*45)*(.035 if variant=='a' else .065)
        fade=min(1,t/2,(32-t)/2)
        samples.append((pad+kick+melody*hook+hat)*fade)
    with wave.open(str(root/f'demo-{variant}.wav'),'wb') as w:
        w.setparams((1,2,rate,0,'NONE','not compressed'))
        w.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,x))*26000)) for x in samples))
    peaks=[round(max(abs(x) for x in samples[j*len(samples)//100:(j+1)*len(samples)//100]),4) for j in range(100)]
    (root/f'peaks-{variant}.json').write_text(json.dumps(peaks))
print('Created three distinct 32-second original instrumental fixtures.')
