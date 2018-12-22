import struct


def packetize(num):
    return struct.pack("<I",num)

def unpacketize(packet):
    return struct.unpack("<I",packet)



seq_number = packetize(5)

checksum = packetize(10)

data  = "Selamun aleykum broo"

message = seq_number + checksum + data


value = unpacketize(message[:4])
value2 = unpacketize(message[4:8])

payload = message [8:]

print value[0] , value2[0] , payload

