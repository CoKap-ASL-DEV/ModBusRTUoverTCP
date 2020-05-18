#!/usr/bin/python
# -*- coding: utf-8 -*-

# 관련라이브러리 : struct(https://docs.python.org/2/library/struct.html)
# 프로토콜 :  modbus TCP
# 기능 : 멀티어드레스 read, 싱글어드레스 write

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


def set_modbus_request(devAddr, fCode, sAddr, qnty):
	if sAddr > 10000:
		sAddr = sAddr % 10000 - 1
		
	##### RTU Protocol 형식 : Device Address(1) 1~247,    Fucntion Code(1),   Starting Address(2),   Quantity of input register(2),   crc(2)

	#### SEND: 0x1 0x4 0x0 0x0 0x0 0x4
	devAddr = 0x01
	fCode = 0x04
	sAddr1 = sAddr>>16
	sAddr2 = (sAddr & 0xff00) >>8
	sAddr3 = (sAddr & 0xff)	
	qnty = 0x07
	#crc = 0xf1c9
	crcInput = bytes([devAddr,fCode,sAddr1,sAddr2,sAddr3,qnty])
	crcRes = crc16(crcInput)
	crcFirstbytes = crcRes & 0xff
	crcSecondbytes = crcRes>>8
	
	
	packet = struct.pack(">BBHHBB", devAddr, fCode, sAddr, qnty, crcFirstbytes,crcSecondbytes)   	
	#packet = struct.pack(">BBHHH", devAddr, fCode, sAddr, qnty, crc)   	
	return packet
	##length(2) 인데 BB 두개로 잡아놓은듯
	###length => 6 -> unit(1), cmd(1), addr(2), cnt(2)

# struct.pack(fmt, v1, v2, ...)  fmt
# Return a string containing the values v1, v2, ... packed according to the given format. The arguments must match the values required by the format exactly.


def usage(myname):
	temp = myname.split('\\')  ### \\로 구분된 경로를 나눠줌
	tlen = len(temp)
	print("-----  usage  -----")
	print("read : %s r 1 30007 20" % (temp[tlen - 1]))

	print("write : %s w 1 40001 0xAADD" % (temp[tlen - 1]))
	sys.exit(0)

def send_request(devAddr, sAddr, qnty):
	fCode = 4
	# if (saddr / 10000) == 3 :
	# 	scmd = 4
	# elif (saddr / 10000) == 4:
	# 	scmd = 3
	### scmd -> cmd --> Function Code

	print("send command : %d (%d)" % (fCode, sAddr))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDR)


#### sbuf 가 발송하는 패킷
	sbuf = set_modbus_request(devAddr, fCode, sAddr, qnty)   #### sbuf 가 발송하는 패킷
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
	recv_devAddr = struct.unpack('>B', rbuf[0:1])[0]
	recv_fcode = struct.unpack('>B', rbuf[1:2])[0]
	recv_ByteCount = struct.unpack('>B', rbuf[2:3])[0]
	Data1 = struct.unpack('>H', rbuf[3:5])[0]
	Data2 = struct.unpack('>H', rbuf[5:7])[0]
	Data3 = struct.unpack('>H', rbuf[7:9])[0]
	Data4 = struct.unpack('>H', rbuf[9:11])[0]
	Data5 = struct.unpack('>H', rbuf[11:13])[0]
	Data6 = struct.unpack('>H', rbuf[13:15])[0]
	Data7 = struct.unpack('>H', rbuf[15:17])[0]
	
	# runit = struct.unpack('>B', rbuf[6:7])[0]
	# rcmd = struct.unpack('>B', rbuf[7:8])[0]
	# rdsize = struct.unpack('>B', rbuf[8:9])[0]
	# buf_size = struct.calcsize(rbuf)
	print("recv_devAddr : %d" % (recv_devAddr))
	print("recv_fcode : %d" % (recv_fcode))
	print("recv_ByteCount : %d" % (recv_ByteCount))
	print("Data1 : %d" % (Data1))
	print("Data2 : %d" % (Data2))
	print("Data3 : %d" % (Data3))
	print("Data4 : %d" % (Data4))
	print("Data5 : %d" % (Data5))
	print("Data6 : %d" % (Data6))
	print("Data7 : %d" % (Data7))
	# print("buf size : %d" % (len(rbuf)))
	#print ("[%d] recv size : %d, unit id : %d, cmd : %d, data size : %d" % (len(rbuf), rsize, runit, rcmd, rdsize))



	
	for i in range(3, int(recv_ByteCount)+3):
		#print(i)
		if ( i % 2) :
			b = struct.unpack('>H', rbuf[i:i+2])[0]
			print(b)
			


	# for i in range(3, int(recv_ByteCount/2)):
	# 	if ( i % 2) :
	# 		b = struct.unpack('>H', rbuf[i:i+2])
	# 		ret = b[0] * 256 + b[1]
	# 		print("[%02d] %d (%02s)" % ((i - 9)/2 + 1, ret, hex(ret)))   ### ★★★★★ ret이 각 레지스터별 리턴 값

#


if __name__ == "__main__":

	HOST = '127.0.0.1'
	PORT = 502
	ADDR = (HOST, PORT)
	BUFSIZE = 4096

	log.debug("---------------------------")
	log.debug(sys.argv)
	log.debug("---------------------------")

	alen = len(sys.argv)

	if alen < 2:
		usage(sys.argv[0])
	else:
		rw_mode = sys.argv[1]   ## r : Read, w : Write 
		devAddr = int(sys.argv[2]) ## 
		sAddr = int(sys.argv[3])

	scmd = 0

	if ( rw_mode == "r" ):
		qnty = int(sys.argv[4])
		send_request(devAddr, sAddr, qnty)

	sys.exit(0)


##### RTU Protocol 형식 : Device Address(1) 1~247,    Fucntion Code(1),   Starting Address(2),   Quantity of input register(2),   crc(2)
##### 시뮬레이터 활용 했을때의 송수신 데이터 및 CRC 데이터
	#### SEND: 0x1 0x4 0x0 0x0 0x0 0x4                                0xf1 0xc9
	#### RECV: 0x1 0x4 0x8 0x0 0x1 0x0 0x2 0x0 0x3 0x0 0x4            0xbc 0xce


	### SEND : b'\x01\x04\x00\x00\x00\x04\xf1\xc9'