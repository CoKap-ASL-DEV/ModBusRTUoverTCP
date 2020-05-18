from crc162 import crc16
import math
myname = "d:\\dev\\ModbusTcp\\moudbus_rw_test.py"
temp = myname.split('\\')
# a = crc16(b'\x01\x04\x08\x00\x01\x00\x02\x00\x03\x00\x04')
devAddr = 0x01
fCode = 0x04
sAddr = 0x123456

sAddr1 = sAddr>>16
sAddr2 = (sAddr & 0xff00) >>8
sAddr3 = (sAddr & 0xff)
qnty = 0x04	

#crcInput = bytes([devAddr,fCode,sAddr1,sAddr2,sAddr3,qnty])

#crcRes = crc16(crcInput)
#crcFirstbytes = crcRes & 0xff
#crcSecondbytes = crcRes>>8
#print(temp)
#print(a)
# print(crcFirstbytes)
# print(crcSecondbytes)


# print((sAddr1) )
# print((sAddr2) )
# print((sAddr3) )
# print("%2x" %(sAddr1) )
# print("%2x" %(sAddr2) )
# print("%2x" %(sAddr3) )




addr = 1230
lenaddr = len(str(addr))
addrSeparate = []

for i in range(lenaddr):    
    temp = addr % 10
    addrSeparate.append(temp)
    addr = addr // 10
print(addrSeparate) ##reverse order    
sum = 0 
for i in range(len(addrSeparate),0,-1):       
    sum += 10**(i-1)*addrSeparate.pop()        
print(sum)


def idSeperate(id):
    lenID = len(str(id))
    idSeparateList = []
    idInt = id
    for i in range(lenID):    
        temp = idInt % 10
        idSeparateList.append(temp)
        idInt = idInt // 10
    print(idSeparateList) ##reverse order    
    return idSeparateList

idsep = idSeperate(123)
# abc = chr(0x31)
print(idsep)
