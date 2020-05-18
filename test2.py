a1 = 0x31 ## (1)
a2 = 0x31 ## (1)
a3 = 0x38 ## (8)
a4 = 0x30 ## (0)


b1 = 0x2B ## (-)  (+)0x2B (-)0x2D
b2 = 0x30 ## (0)
b3 = 0x30 ## (0)
b4 = 0x35 ## (5)

#print(chr(a))

def solarAsciitoInt(s1,s2,s3,s4):
    solarStr = chr(s1) + chr(s2)+chr(s3) + chr(s4)
    soloarInt = int(solarStr)    
    #print(soloarInt)
    return soloarInt


solarRadition = solarAsciitoInt(a1,a2,a3,a4)

print(solarRadition)
print(type(solarRadition))


def temperAsciitoFloat(t1, t2, t3, t4):
    temperStr = chr(t1) + chr(t2)+chr(t3) +"."+ chr(t4)
    temperFloat = float(temperStr)    
    #print(soloarInt)
    return temperFloat


def humidityAsciitoFloat(h1, h2, h3):
    humidityStr = chr(h1) + chr(h2)+"."+ chr(h3)
    humidityFloat = float(humidityStr)    
    #print(soloarInt)
    return humidityFloat


flt = temperAsciitoFloat(b1,b2,b3,b4)
print(flt)
print(type(flt))


flt2 = humidityAsciitoFloat(b2,b3,b4)
print(flt2)
print(type(flt2))