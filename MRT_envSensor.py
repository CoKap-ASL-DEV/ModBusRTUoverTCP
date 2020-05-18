#!/usr/bin/python
# -*- coding: utf-8 -*-

# 관련라이브러리 : struct(https://docs.python.org/2/library/struct.html)

#endianness = [
#    ('@', 'native, native'),
#    ('=', 'native, standard'),
#    ('<', 'little-endian'),
#    ('>', 'big-endian'),
#    ('!', 'network'),
#    ]

# Format		Ctype					python type				standard size
#   H			unsigned short			  integer					  2			
#   B			unsigned char			  integer					  1byte(8bit)			

# transaction = 0x0001
# identifier = 0x0000
# length = 0x0006
# unitid = 0x11
# fcode = 0x03  # Holding register fcode.
# reg_addr = 0x006B  # Register address.
# count = 0x0003  # Read three register.

# pack_ = struct.pack(
#    '>HHHBBHH', transaction, identifier, length, unitid, fcode, reg_addr, count
# )

# transaction is 2Byte == Short == H
# identifier is 2Byte == Short == H
# length is 2Byte == Short == H
# unitid is 1Byte == B
# fcode is 1Byte == B
# reg_addr is 2Byte == Short == H
# count is 2Byte == Short == H

# Thus, the format will be like this >HHHBBHH



# Send 코드 데이터는 아스키 코드 사용

# 어드레스 0번으로 데이터 요청
#  시작문자   읽기(R)    환경(E)   데이터1      데이터2     데이터3    종료문자  Chk
#  0x02   0x52(R)   0x45(E)   0x30(0)   0x30(0)   0x30(0)   0x03   2C
# 시작문자~종료문자까지 hex값을 더하면 12C 뒤 두자리만 사용

# 어드레스 1번으로 데이터 요청
#  시작문자   읽기(R)    환경(E)   데이터1      데이터2     데이터3    종료문자  Chk
#  0x02   0x52(R)   0x45(E)   0x30(0)   0x30(0)   0x31(1)   0x03   2D
# 시작문자~종료문자까지 hex값을 더하면 12D 뒤 두자리만 사용

import binascii
import socket
import struct
import sys
import select
import time
import logging
from crc162 import crc16
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)



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

def calcChkCode(sum):
    chkTmp = sum & 0xFF
    chk = chkTmp
    if(chkTmp==0x02):
        chk=0x04    
    if(chkTmp==0x03):
        chk=0x05
    return chk

def set_mrt_request(id):			
    startChr = 0x02
    comCode = 0x52 #(R)
    typeChr = 0x45 #(E)    
    idSep = idSeperate(id)
    iD100 = hex(idSep[0]) #(0)  100자리
    iD10 = hex(idSep[1]) #(0)   10자리
    iD1 = hex(idSep[2]) #(1)    1자리
    #################################
    endChr = 0x03

    chk = calcChkCode(startChr+comCode+typeChr+iD100+iD10+iD1+endChr)
			
    packet = struct.pack(">BBBBBBBB", startChr,comCode,typeChr,iD100,iD10,iD1,endChr,chk)   	
	
    return packet



def idAsciitoInt(i1,i2,i3):
    idStr = chr(i1) + chr(i2)+chr(i3)
    idInt = int(idStr)    
    #print(soloarInt)
    return idInt


def solarAsciitoInt(s1,s2,s3,s4):
    solarStr = chr(s1) + chr(s2)+chr(s3) + chr(s4)
    soloarInt = int(solarStr)    
    #print(soloarInt)
    return soloarInt

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




def send_request(id):
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDR)

    #### sbuf 가 발송하는 패킷
    sbuf = set_mrt_request(id)   #### sbuf 가 발송하는 패킷
    print("Sended")
    print(repr(sbuf))
    sock.send(sbuf)

    time.sleep (0.05)

    sock.settimeout(3.0)


    #### rbuf 가 수신한 패킷
    rbuf = sock.recv(BUFSIZE)

    sock.close()
    print("Recived")
    print(repr(rbuf))
    ###########################################################
    recv_startChr = struct.unpack('>B', rbuf[0:1])[0]
    recv_comCodee = struct.unpack('>B', rbuf[1:2])[0]
    recv_typeChr = struct.unpack('>B', rbuf[2:3])[0]
    ###########################################################
    idAscii1 = struct.unpack('>B', rbuf[3:4])[0]
    idAscii2 = struct.unpack('>B', rbuf[4:5])[0]
    idAscii3 = struct.unpack('>B', rbuf[5:6])[0]
    ###########################################################
    delimiter1 = struct.unpack('>B', rbuf[6:7])[0]
    ###########################################################
    solarAscii1 = struct.unpack('>B', rbuf[7:8])[0]
    solarAscii2 = struct.unpack('>B', rbuf[8:9])[0]
    solarAscii3 = struct.unpack('>B', rbuf[9:10])[0]
    solarAscii4 = struct.unpack('>B', rbuf[10:11])[0]    
    ###########################################################
    delimiter2 = struct.unpack('>B', rbuf[11:12])[0]
    ###########################################################
    temperAscii1 = struct.unpack('>B', rbuf[12:13])[0]
    temperAscii2 = struct.unpack('>B', rbuf[13:14])[0]
    temperAscii3 = struct.unpack('>B', rbuf[14:15])[0]
    temperAscii4 = struct.unpack('>B', rbuf[15:16])[0]
    ###########################################################
    delimiter3 = struct.unpack('>B', rbuf[16:17])[0]
    ###########################################################
    humidityAscii1 = struct.unpack('>B', rbuf[17:18])[0]
    humidityAscii2 = struct.unpack('>B', rbuf[18:19])[0]
    humidityAscii3 = struct.unpack('>B', rbuf[19:20])[0]
    ###########################################################
    recv_endChr = struct.unpack('>B', rbuf[20:21])[0]
    ###########################################################
    recv_chk = struct.unpack('>B', rbuf[21:22])[0]
    ###########################################################

    idInt = idAsciitoInt(idAscii1, idAscii2, idAscii3) 
    solarRadiation = solarAsciitoInt(solarAscii1, solarAscii2, solarAscii3, solarAscii4)
    temperature = temperAsciitoFloat(temperAscii1, temperAscii2, temperAscii3)
    humidity = humidityAsciitoFloat(humidityAscii1, humidityAscii2, humidityAscii3)
    




if __name__ == "__main__":

	HOST = '127.0.0.1'
	PORT = 502
	ADDR = (HOST, PORT)
	BUFSIZE = 4096

	
	send_request(id)
