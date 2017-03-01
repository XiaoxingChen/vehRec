import os
import sys
import socket
import struct
import time
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

targetAddress = '192.168.1.4'
# targetAddress = '58.196.137.213'
targetPort = 5003

ACK = b'\x79'
NACK = b'\x1F'

RECV_SIZE = 100
SEND_DATA_LEN = 256

byteJump2BootLoader = bytearray(b'\x07\x00\x00\x00\xff\xff\xff\xff')
byteStart = bytearray(b'\x31\xCE')
byteGetFirmwareVersion = bytearray(b'\x01\xFE')
lastedFirmwareVersion = 0x12
oriDownloadAddress = 0x08010000

if len(sys.argv) < 2:
    print('no binary file specified.')
    sys.exit()

fname = sys.argv[1]

#get extension name
tail = fname[-4:]
if tail != ".bin":
    print("the extension is not .bin")
    sys.exit()

# get file, read only, binary
f = open(fname,'rb')
data = f.read()

# establish socket
address = (targetAddress,targetPort)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

##main logic
def sendto_stm32(byte_msg):
    s.sendto(byte_msg,address)

def confirm_ack():
    stmback = s.recvfrom(RECV_SIZE)
    if stmback[0] != ACK:
        return False
    else:
        return True

def getXor(val):
    xor = 0
    for byte in val:
        xor ^= byte
    return xor

def getBytesFromUint32(val):
    val0 = val & 0xFF
    val1 = (val & 0xFF00) >> 8
    val2 = (val & 0xFF0000) >> 16
    val3 = (val & 0xFF000000) >> 24
    return bytearray([val3,val2,val1,val0])

#jump to bootloader
print('jump to bootloader')
sys.stdout.flush()
s.sendto(byteJump2BootLoader,address)
stmback = s.recvfrom(RECV_SIZE)
if stmback[0] == NACK:
    print('already in bootloader')
    sys.stdout.flush()
    stmback = s.recvfrom(RECV_SIZE)
    stmback = s.recvfrom(RECV_SIZE)
    stmback = s.recvfrom(RECV_SIZE)
elif stmback[0] == b'\x07\x00\x00\x00':
    print('now in application')
    sys.stdout.flush()
    time.sleep(1)
else:
    print('get byte', stmback[0])

s.sendto(byteGetFirmwareVersion,address)
stmback = s.recvfrom(RECV_SIZE)

isVersionMatch = False
if(len(stmback[0]) > 1): #beforeV1.3
    while(stmback[0][0] != ACK[0]):
        s.sendto(byteGetFirmwareVersion,address)
        stmback = s.recvfrom(RECV_SIZE)
        print('require firmware version')
        sys.stdout.flush()
        time.sleep(1)
    print('firmware version:V%d.%d' %(stmback[0][1] >> 4, stmback[0][1] & 0xF))
    if(stmback[0][1] == lastedFirmwareVersion):
        isVersionMatch = True
        
else: #since V1.3
    while(stmback[0][0] != ACK[0]):
        s.sendto(byteGetFirmwareVersion,address)
        stmback = s.recvfrom(RECV_SIZE)
        print('get firmware version')
        sys.stdout.flush()
        time.sleep(1)
    stmback = s.recvfrom(RECV_SIZE)
    print('firmware version:V%d.%d' %(stmback[0][0] >> 4, stmback[0][0] & 0xF))
    if(stmback[0][0] == lastedFirmwareVersion):
        isVersionMatch = True
        
if(not isVersionMatch):
    print('the latesd version is V%d.%d' %(lastedFirmwareVersion >>4, lastedFirmwareVersion & 0xF))
    print('do you want to continue? y/n')
    sys.stdout.flush()
    if('y' != input()):
        quit()

i = 0
length = len(data)
while i < length:
    nowDownloadAddress = oriDownloadAddress + i
    print("write address 0x%X" % nowDownloadAddress)
    sys.stdout.flush()
    j = i + SEND_DATA_LEN
    if j > length:
        j = length
    slip = data[i:j]
    slipLen = j - i
    slipArray = bytearray(slip)
    slipArray.insert(0,slipLen - 1)
    slipArray.append(getXor(slipArray))

    # send head
    sendto_stm32(byteStart)
    if confirm_ack() != True:
        continue

    #send address
    byteAddress = getBytesFromUint32(nowDownloadAddress)
    byteAddress.append(getXor(byteAddress))
    sendto_stm32(byteAddress)
    if confirm_ack() != True:
        continue

    #send data
    sendto_stm32(slipArray)
    if confirm_ack() != True:
        continue

    i = j
    
#time.sleep(1)    
sendto_stm32(b'\x31\xce\x08\x00\xc0\x00\xc8\x03\xaa\xaa\x55\x55\x03')
sendto_stm32(b'\x21\xde\x08\x01\x00\x00\x09')
print('down load over')
sys.stdout.flush()
os.system('pause')




