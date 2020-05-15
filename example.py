# MODBUS TCP/IP Packet Structure

# The next thing I needed to know was the structure for Modbus packets. Thankfully they are quite simple, made up of a small header containing information such as length, destination unit identifier and function code, followed by the data:

# byte 0 : Transaction identifier – copied by server – usually 0
# byte 1 : Transaction identifier – copied by server – usually 0
# byte 2 : Protocol identifier = 0
# byte 3 : Protocol identifier = 0
# byte 4 : Length field (upper byte) = 0 (since all messages are smaller than 256)
# byte 5 : Length field (lower byte) = number of bytes following
# byte 6 : Unit identifier (previously ‘slave address’)
# byte 7 : MODBUS function code
# byte 8+ : Data as needed
# Byte 7 above contains the ‘Function Code’, these codes instruct the destination on whether the requester is asking to read or write to one of the 4 Modbus registers described previously:

# 1 : Read coils
# 2 : Read input discretes
# 3 : Read multiple registers
# 4 : Read input registers
# 5 : Write coil
# 6 : Write single register
# 7 : Read exception status
# 16: Write multiple registers
# The following is an example Modbus packet:

# ?
# 1
# 00, 00, 00, 00, 00, 06, 10, 05, 00, 01, FF, 00
# 00 : Transaction ID
# 00 : Transaction ID
# 00 : Protocol ID
# 00 : Protocol ID
# 00:
# 06 : The following packet contains 6 bytes.
# 10 : Destination unit 16 (Hex 10).
# 05 : Write a single coil (Function Code 5).
# 00 :
# 01 : Set coil address #1.
# FF : Value High (On).
# 00:

import socket
import struct
import time
 
# Create a TCP/IP socket
TCP_IP = '192.168.0.107'
TCP_PORT = 502
BUFFER_SIZE = 39
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
 
try:
    # Switch Plug On then Off
    unitId = 16 # Plug Socket
    functionCode = 5 # Write coil
    
    print("\nSwitching Plug ON...")
    coilId = 1
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    print("TX: (%s)" %req)
    rec = sock.recv(BUFFER_SIZE)
    print("RX: (%s)" %rec)
    time.sleep(2)
    
    print("\nSwitching Plug OFF...")
    coilId = 2
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    print("TX: (%s)" %req)
    rec = sock.recv(BUFFER_SIZE)
    print("RX: (%s)" %rec)
    time.sleep(2)
 
finally:
    print('\nCLOSING SOCKET')
    sock.close()