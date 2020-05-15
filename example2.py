# At first you can use pymodbus library with very features.
# Also struct.pack() not support a list as argument.
# 0001 0000 0006 11 03 006B 0003 is a standard example of Modbus-TCP packet which contained:
# 0001: Transaction Identifier

# 0000: Protocol Identifier

# 0006: Message Length (6 bytes to follow)

# 11: The Unit Identifier  (17 = 11 hex)

# 03: The Function Code (read Analog Output Holding Registers)

# 006B: The Data Address of the first register requested. (40108-40001 = 107 =6B hex)

# 0003: The total number of registers requested. (read 3 registers 40108 to 40110)

# Reference

# Thus, you can create a Modbus-TCP packet with the above example:

import struct

transaction = 0x0001
identifier = 0x0000
length = 0x0006
unitid = 0x11
fcode = 0x03  # Holding register fcode.
reg_addr = 0x006B  # Register address.
count = 0x0003  # Read three register.


total_pack_string = '0x{:04x}{:04x}{:04x}{:02x}{:02x}{:04x}{:04x}'.format(
    transaction, identifier, length, unitid, fcode, reg_addr, count
)
total_pack_hex = hex(int(total_pack_string, 16))

'''Or with using pack method.'''
pack_ = struct.pack(
   '>HHHBBHH', transaction, identifier, length, unitid, fcode, reg_addr, count
)

# Then send the pack_ or total_pack_hex using a TCP-Socket.
# [NOTE]:

# transaction is 2Byte == Short == H
# identifier is 2Byte == Short == H
# length is 2Byte == Short == H
# unitid is 1Byte == B
# fcode is 1Byte == B
# reg_addr is 2Byte == Short == H
# count is 2Byte == Short == H


# B is unsigned byte
# H is unsigned short
# Thus, the format will be like this >HHHBBHH

