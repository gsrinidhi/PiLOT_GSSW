import socket
fname = "PILOT_DATA_Initial"

hk_count = 1
hk_error = 0
aris_count = 1
aris_error = 0
thermistor_count = 1
thermistor_error_count = 0
hk_pkt_len = 107
aris_pkt_len = 242
thermistor_pkt_len = 68
logs_pkt_len = 116
time_pkt_len = 39
def decode_hk_pkt(bytestream):
    global hk_count
    global hk_error
    sumA = 0
    sumB = 0
    print("HK Length = " + str(len(bytestream)))
    for id in range(len(bytestream)-2):
        d = bytestream[id]
        sumA = (sumA + d) % 255
        sumB = (sumA + sumB) % 255
    temp = 255 - ((sumA + sumB) % 255)
    sumB = 255 - ((sumA + temp) % 255)
    print("HK count = " + str(hk_count))
    #print(bytestream)
    if temp == bytestream[-2] and sumB == bytestream[-1]:
        print(" HK decode successful")
        send_to_COSMSOS(bytestream)
    else:
        print(" HK Fletcher fail")
        print(" temp = " + str(temp))
        print(" sumb = " + str(sumB))
        print(" bytestream[-2] = " + str(bytestream[-2]))
        print(" bytestream[-1] = " + str(bytestream[-3]))
        
        hk_error = hk_error + 1
    
    hk_count = hk_count + 1
    return 0
def decode_aris_pkt(bytestream):
    global aris_count
    global aris_error
    sumA = 0
    sumB = 0
    print("HK Length = " + str(len(bytestream)))
    for id in range(len(bytestream)-2):
        d = bytestream[id]
        sumA = (sumA + d) % 255
        sumB = (sumA + sumB) % 255
    temp = 255 - ((sumA + sumB) % 255)
    sumB = 255 - ((sumA + temp) % 255)
    print("ARIS count = " + str(aris_count))
    #print(bytestream)
    if temp == bytestream[-2] and sumB == bytestream[-1]:
        print(" ARIS decode successful")
        send_to_COSMSOS(bytestream)
        
    else:
        print(" ARIS Fletcher fail")
        print(" temp = " + str(temp))
        print(" sumb = " + str(sumB))
        print(" bytestream[-2] = " + str(bytestream[-2]))
        print(" bytestream[-1] = " + str(bytestream[-3]))
        #send_to_COSMSOS(bytestream)
        aris_error = aris_error + 1
    
    aris_count = aris_count + 1
    return 0

def decode_payload_pkt(bytestream):
    global thermistor_count
    global thermistor_error_count
    sumA = 0
    sumB = 0
    print("HK Length = " + str(len(bytestream)))
    for id in range(len(bytestream)-2):
        d = bytestream[id]
        sumA = (sumA + d) % 255
        sumB = (sumA + sumB) % 255
    temp = 255 - ((sumA + sumB) % 255)
    sumB = 255 - ((sumA + temp) % 255)
    print("Thermistor count = " + str(thermistor_count))
    #print(bytestream)
    if temp == bytestream[-2] and sumB == bytestream[-1]:
        print(" Thermistor decode successful")
        send_to_COSMSOS(bytestream)
    else:
        print(" Thermistor Fletcher fail")
        print(" temp = " + str(temp))
        print(" sumb = " + str(sumB))
        print(" bytestream[-2] = " + str(bytestream[-2]))
        print(" bytestream[-1] = " + str(bytestream[-3]))
        #send_to_COSMSOS(bytestream)
        thermistor_error_count = thermistor_error_count + 1
    
    thermistor_count = thermistor_count + 1
    return 0
def separate_packets(bytestream):
    i = 0
    while 1:
        if i < (len(bytestream)-aris_pkt_len - 1):
            if bytestream[i] == 0x08 and bytestream[i+1] == 0x0A :
                decode_hk_pkt(bytestream[i:i+hk_pkt_len])
                i = i + hk_pkt_len
            elif bytestream[i] == 0x08 and bytestream[i+1] == 0x32:
                decode_aris_pkt(bytestream[i:i+aris_pkt_len])
                i = i + aris_pkt_len
            elif bytestream[i] == 0x08 and bytestream[i+1] == 0x14:
                decode_payload_pkt(bytestream[i:i+thermistor_pkt_len])
                i = i + thermistor_pkt_len
            else:
                i = i + 1
            #i = i + 1
        else:
            break
def send_to_COSMSOS(bytestream):
    #tx = bytestream
    tx = str(bytestream)
    tx = tx.encode()
    tx = bytes(bytestream)
    HOST = "127.0.0.1"
    PORT = 27015
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.send(tx)
f = open(fname,'rb')
bytestream = []
i = 0
count = 0
ecount = 0
p_count = 0
while 1:
    c = f.read(1)
    if not c:
        break
    c = f.read(1)
    if not c:
        break
    i = int.from_bytes(c,"big")
    print(i)
    # k = input("Test data")
    bytestream.append(i)

# while 1:
#     c = f.read(1)
#     ij = int.from_bytes(c,"big")
#     i = ij >> 4
#     if not c:
#         break
#     if i != 8:
#         c = f.read(1)
#         c = f.read(1)
#         c1 = int.from_bytes(c,"little")
#         bytestream.append(c1)
#         #bytestream.append(int(c,16))

#         count = count + 1
#         if count % 1000 == 0:
#             print(type(c))
#             print("Working")
#         c = f.read(1)
#         if i != 2:
#             print("Value = " + hex(ij))
#     else:
#         c = f.read(1)
#         c = f.read(1)
#         i1 = int.from_bytes(c,"little")
#         c = f.read(1)
#         i2 = int.from_bytes(c,"little")
#         if i1 != 1 and i2 != 255:
#             print("Error")
#             print("Ecount = " + str(ecount))
#     i = i+1
#     ecount = ecount + 4
separate_packets(bytestream)

print("Total hk = " + str(hk_count))
print("Error hk = " + str(hk_error))
print("Total aris = " + str(aris_count))
print("Error aris = " + str(aris_error))
print("Total Thermistor = " + str(thermistor_count))
print("Error Thermistor = " + str(thermistor_error_count))
#send_to_COSMSOS(bytestream)

# prev = 0
# next = 0
# total = 0
# ecount = 0
# while 1:
#     c = f.read(1)
#     ij = int.from_bytes(c,"big")
#     i = ij >> 4
#     if not c:
#         break
#     if i != 8:
#         c = f.read(1)
#         c = f.read(2)
#         cn = int.from_bytes(c,"big")
#         #print(cn)
#         next = cn
#         if (next - prev) > 1 and prev != 0:
#             print("error")
#             ecount = ecount + 1
#         prev = cn
#         total = total + 1
#     else:
#         c = f.read(3)

# print("Done")
# print("Total = " + str(total))
# print("error = " + str(ecount))

    