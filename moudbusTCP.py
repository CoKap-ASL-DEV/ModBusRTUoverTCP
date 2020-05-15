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
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def set_modbus_request(unit, cmd, addr, cnt):
	if addr > 10000:
		addr = addr % 10000 - 1
	# transaction identifier (2), protocol identifier (2), length (2), 
	packet = struct.pack(">HHHBBHH", 0, 0, 6, unit, cmd, addr, cnt)   	
	return packet
	##length(2) 인데 BB 두개로 잡아놓은듯
	###length => 6 -> unit(1), cmd(1), addr(2), cnt(2)

# struct.pack(fmt, v1, v2, ...)  fmt
# Return a string containing the values v1, v2, ... packed according to the given format. The arguments must match the values required by the format exactly.

def set_modbus_write(unit, cmd, addr, val):
	if addr > 10000:
		addr = addr % 10000 - 1
	# transaction identifier (2), protocol identifier (2), length (2), 
	packet = struct.pack(">HHBBBBHH", 0, 0, 0, 6, unit, cmd, addr, val)
	return packet

def usage(myname):
	temp = myname.split('\\')  ### \\로 구분된 경로를 나눠줌
	tlen = len(temp)
	print("-----  usage  -----")
	print("read : %s r 1 30007 20" % (temp[tlen - 1]))
	print("write : %s w 1 40001 0xAADD" % (temp[tlen - 1]))
	sys.exit(0)

def send_request(sunit, saddr, scnt):
	scmd = 4
	if (saddr / 10000) == 3 :
		scmd = 4
	elif (saddr / 10000) == 4:
		scmd = 3
	### scmd -> cmd --> Function Code

	print("send command : %d (%d)" % (scmd, saddr))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDR)


#### sbuf 가 발송하는 패킷
	sbuf = set_modbus_request(sunit, scmd, saddr, scnt)   #### sbuf 가 발송하는 패킷
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

	rsize = struct.unpack('>B', rbuf[5:6])[0]
	runit = struct.unpack('>B', rbuf[6:7])[0]
	rcmd = struct.unpack('>B', rbuf[7:8])[0]
	rdsize = struct.unpack('>B', rbuf[8:9])[0]
	buf_size = struct.calcsize(rbuf)
	print("recv size : %d" % (rsize))
	print("buf size : %d" % (len(rbuf)))
	#print ("[%d] recv size : %d, unit id : %d, cmd : %d, data size : %d" % (len(rbuf), rsize, runit, rcmd, rdsize))

	for i in range(9, len(rbuf)):
		if ( i % 2) :
			b = struct.unpack('>BB', rbuf[i:i+2])
			ret = b[0] * 256 + b[1]
			print("[%02d] %d (%02s)" % ((i - 9)/2 + 1, ret, hex(ret)))   ### ★★★★★ ret이 각 레지스터별 리턴 값

#
#
def send_write(sunit, saddr, scnt):
	if (saddr / 10000) == 4 :
		scmd = 6
	
	print("send command : %d, read value : %x" % (scmd, scnt))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDR)

	sbuf = set_modbus_write(sunit, scmd, saddr, scnt)
	print(repr(sbuf))
	sock.send(sbuf)

	time.sleep (0.05)

	sock.settimeout(3.0)
	rbuf = sock.recv(BUFSIZE)

	sock.close()

	print(repr(rbuf))

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
		sunit = int(sys.argv[2]) ## 
		saddr = int(sys.argv[3])

	scmd = 0

	if ( rw_mode == "r" ):
		scnt = int(sys.argv[4])
		send_request(sunit, saddr, scnt)

	# write modbus
	elif (rw_mode == "w"):
		if len(sys.argv[4]) > 1 and sys.argv[4][0:2] == '0x':
			h = sys.argv[4][2:]
			if len(h) % 2:
				h = "0" + h
			scnt = int(h, 16)
		else:
			scnt = int(sys.argv[4])

		print("read value : %d(%s)" % (scnt, struct.pack('>H', scnt)))

		send_write(sunit, saddr, scnt)

		print("write >>>>>>>>>>>>>>>>>>>>>\n")

		time.sleep(0.5)

		send_request(sunit, saddr, 1)

	sys.exit(0)
