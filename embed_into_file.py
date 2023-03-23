import mido
print(mido.get_output_names())
from mido import MidiFile, MidiTrack
#outport = mido.open_output('USB MIDI Interface 2')
import os
import PIL
from PIL import Image
import time



infile=MidiFile('BadAppleAmenBreak.mid')

with open('labels.txt','r') as f:
    labels=f.readlines()
spf=infile.ticks_per_beat/12
#138bpm
    #2.3bps
    #9.2 *4
    #18.4 *8
    #27.6 * 12!!
    #12fpb/27.6fps

#tryna convert ticks to uh fucking uh
#like time
#idk

labs=[]
t=0
stp=False
trark=MidiTrack()
infile.tracks.append(trark)
for i in labels:
    #print(i)
    if stp: t=stp
    stp=float(i.split('\t')[0])
    dlt=stp-t
    text=str(i.split('\t')[2])[:15]
    dlt=int(dlt*spf*27.6*1.004000/1.00080611)
    #print(spf*27.6)
    #print(dlt)
    #print(text)



    #Text F0 41 10 45 12 10 00 00 50 4F 52 4E 31 F7
    sysex=['41','10','45','12','10','00','00']
    string=text
    deet=[]
    #sooo its expecting data to be hex formatted ok so
    for i in string:
        deet.append(format(ord(i), "x").zfill(2).upper())
    for i in deet:
        sysex.append(i)
    #print(sysex)
    address1=int('10',base=16)
    address2=int('00',base=16)
    address3=int('00',base=16)
    data=0
    for i in deet:
        data+=int(i,base=16)
    chk=(128 - (address1+address2+address3+data)) % 128
    sysex.append(format(chk, 'x').zfill(2).upper())


    sysex_dec=[]
    for i in sysex:
        sysex_dec.append(int(i,base=16))
    #print(sysex)
    trark.append(mido.Message('sysex',data=sysex_dec, time=dlt))


#F0 - Exclusive Status

#41 - ID
#10 - Device IC
#45 - Model ID
#12 - Command ID

#10 01 00 - Address

#00 0F 06 06 06 06 06 06
#06 06 06 06 06 0F 00 00
#00 13 19 0D 0D 0D 0D 0D
#0D 0D 0D 0D 19 13 00 00
#00 1E 13 13 13 13 13 1E
#13 13 13 13 13 1E 00 00
#00 00 00 00 00 00 00 00
#00 00 00 00 00 00 00 00
import random
deet=['00', '0F', '06', '06', '06', '06', '06', '06', '06', '06', '06', '06', '06', '0F', '00', '00', '00', '13', '19', '0D', '0D', '0D', '0D', '0D', '0D', '0D', '0D', '0D', '19', '13', '00', '00', '00', '1E', '13', '13', '13', '13', '13', '1E', '13', '13', '13', '13', '13', '1E', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
print(len(deet))
#2A - Checksum!

#Text F0 41 10 45 12 10 00 00 50 4F 52 4E 31 F7
#st=time.time()
opixelsum=0
pixelsum=0
for framp in range(1,len(os.listdir('in'))):
    #print(i)
    #et=time.time()-st
    trueframe=int(framp*(30/27.6))+1#((int(et*30))+1)
    try:
        q=Image.open('in\\'+str(trueframe).zfill(4)+'.png')
    except:
        pass
    #q=Image.open('in\\3232.png')

    deet=[]
    opixelsum=pixelsum
    pixelsum=0
    for x1 in range(0,3):
        for y in range(16):
            byte=['0','0','0']
            for x in range(x1*5,x1*5+5):
                yeah=q.getpixel((x*2,y))
                togo='1'
                if yeah==255:
                    togo='0'
                byte.append(togo)
                pixelsum+=yeah
            grape=''.join(byte)
            deet.append(format(int(grape,2), 'x').zfill(2).upper())

    
    for y in range(16):
        byte=['0','0','0']
        yeah=q.getpixel((31,y))
        togo='1'
        if yeah==255:
            togo='0'
        byte.append(togo)
        byte.append(togo)
        byte.append(togo)
        byte.append(togo)
        byte.append(togo)
        grape=''.join(byte)
        #print(grape)
        deet.append(format(int(grape,2), 'x').zfill(2).upper())
            #g=format(random.randrange(0,128), 'x').zfill(2)
            #deet.append(g.upper())
    #F7 - End of Exclusive


    address1=int('10',base=16)
    address2=int('01',base=16)
    address3=int('00',base=16)
    data=0
    for i in deet:
        data+=int(i,base=16)
    chk=(128 - (address1+address2+address3+data)) % 128
    #print(hex(chk))
    sysex=['41','10','45','12','10','01','00']
    for i in deet:
        sysex.append(i)
    sysex.append(format(chk, 'x').zfill(2).upper())
    #sysex.append('F7')
    #print(sysex)

    sysex_dec=[]
    for i in sysex:
        sysex_dec.append(int(i,base=16))
    #print(sysex_dec)
    #138bpm
    #2.3bps
    #9.2 *4
    #18.4 *8
    #27.6 * 12!!
    #12fpb/27.6fps
    
    spf=int(infile.ticks_per_beat/12)
    dif=abs(pixelsum-opixelsum)
    #print('dif: '+str(dif))
    infile.tracks[0].append(mido.Message('sysex',data=sysex_dec, time=spf))
        #outport.send(mido.Message('sysex',data=sysex_dec))

infile.save('BadAppleAmenBreakWithVideo7.mid')
