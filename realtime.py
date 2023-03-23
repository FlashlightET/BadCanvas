import mido
print(mido.get_output_names())
outport = mido.open_output('USB MIDI Interface 2')
import os
import PIL
from PIL import Image
import time

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
st=time.time()
while True:
    #print(i)
    et=time.time()-st
    trueframe=((int(et*30))+1)
    q=Image.open('in\\'+str(trueframe).zfill(4)+'.png')
    #q=Image.open('in\\3232.png')

    deet=[]
    
    for x1 in range(0,3):
        for y in range(16):
            byte=['0','0','0']
            for x in range(x1*5,x1*5+5):
                yeah=q.getpixel((x*2,y))
                togo='1'
                if yeah==255:
                    togo='0'
                byte.append(togo)
            grape=''.join(byte)
            deet.append(format(int(grape,2), 'x').zfill(2).upper())


    for y in range(16):
        byte=['0','0','0']
        yeah=q.getpixel((31,y))
        togo='1'
        if yeah==255:
            togo='0'
        byte.append(togo)
        byte.append(togo)#redundant data
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
    
    outport.send(mido.Message('sysex',data=sysex_dec))

    #Text F0 41 10 45 12 10 00 00 50 4F 52 4E 31 F7
    sysex=['41','10','45','12','10','00','00']
    string=str(et)[:15]
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
    outport.send(mido.Message('sysex',data=sysex_dec))
    #break
