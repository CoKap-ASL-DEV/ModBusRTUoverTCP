''''-*- coding: utf-8 -*-
return 19255 0x4B37 '''
import numpy as np

def crc16(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)

    return np.uint16(crc)
    
# res = crc16(b'\x31\x32\x33\x34\x35\x36\x37\x38\x39')
res = crc16(b'\x01\x04\x00\x00\x00\x04')
print(res)
print ("Returning single value %d %2x %2x" %(res, res & 0xff, res>>8 ))

res = crc16(b'\x01\x04\x08\x00\x01\x00\x02\x00\x03\x00\x04')
print(res)
print ("Returning single value %d %2x %2x" %(res, res & 0xff, res>>8 ))


##### 시뮬레이터 활용 했을때의 송수신 데이터 및 CRC 데이터

#### SEND: 0x1 0x4 0x0 0x0 0x0 0x4                                0xf1 0xc9
#### RECV: 0x1 0x4 0x8 0x0 0x1 0x0 0x2 0x0 0x3 0x0 0x4            0xbc 0xce