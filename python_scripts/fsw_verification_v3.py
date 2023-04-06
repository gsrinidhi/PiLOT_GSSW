import socket
import os
fnames = os.listdir("./")
hk_pkt_len = 107
aris_pkt_len = 242
thermistor_pkt_len = 68
logs_pkt_len = 116
time_pkt_len = 39
fname = "EZ_USB_LOG_POST_RS03.txt"
# dummy_bytes_1 = 43
# dummy_bytes_2 = 16
# dummy_bytes_1 = 15 #Time_test_3
# dummy_bytes_2 = 44
# dummy_bytes_1 = 20 #Time test 4
# dummy_bytes_2 = 39
# dummy_bytes_1 = 37
# dummy_bytes_2 =22
dummy_bytes_1 = 31
dummy_bytes_2 = 28
hk_count = 0
hk_error = 0
aris_count = 0
aris_error = 0
thermistor_count = 0
thermistor_error_count = 0
logs_count = 0
logs_error_count = 0
time_count = 0
time_error = 0
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
        # print(" HK Fletcher fail")
        # print(" temp = " + bin(temp))
        # print(" sumb = " + bin(sumB))
        # print(" bytestream[-2] = " + bin(bytestream[-2]))
        # print(" bytestream[-1] = " + bin(bytestream[-1]))
        #send_to_COSMSOS(bytestream)
        hk_error = hk_error + 1
    
    hk_count = hk_count + 1
    return 0

def decode_time_pkt(bytestream):
    global time_count
    global time_error
    sumA = 0
    sumB = 0
    print("Time Length = " + str(len(bytestream)))
    for id in range(len(bytestream)-2):
        d = bytestream[id]
        sumA = (sumA + d) % 255
        sumB = (sumA + sumB) % 255
    temp = 255 - ((sumA + sumB) % 255)
    sumB = 255 - ((sumA + temp) % 255)
    print("Time count = " + str(hk_count))
    #print(bytestream)
    if temp == bytestream[-2] and sumB == bytestream[-1]:
        print(" Time decode successful")
        send_to_COSMSOS(bytestream)
    else:
        # print(" HK Fletcher fail")
        # print(" temp = " + bin(temp))
        # print(" sumb = " + bin(sumB))
        # print(" bytestream[-2] = " + bin(bytestream[-2]))
        # print(" bytestream[-1] = " + bin(bytestream[-1]))
        #send_to_COSMSOS(bytestream)
        time_error = time_error + 1
    
    time_count = time_count + 1
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
        # print(" ARIS Fletcher fail")
        # print(" temp = " + bin(temp))
        # print(" sumb = " + bin(sumB))
        # print(" bytestream[-2] = " + bin(bytestream[-2]))
        # print(" bytestream[-1] = " + bin(bytestream[-3]))
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
        print(" temp = " + bin(temp))
        print(" sumb = " + bin(sumB))
        print(" bytestream[-2] = " + bin(bytestream[-2]))
        print(" bytestream[-1] = " + bin(bytestream[-3]))
        #send_to_COSMSOS(bytestream)
        thermistor_error_count = thermistor_error_count + 1
    
    thermistor_count = thermistor_count + 1
    return 0

def decode_LOGS_pkt(bytestream):
    global logs_count
    global logs_error_count
    sumA = 0
    sumB = 0
    print("Logs Length = " + str(len(bytestream)))
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
        print(" temp = " + bin(temp))
        print(" sumb = " + bin(sumB))
        print(" bytestream[-2] = " + bin(bytestream[-2]))
        print(" bytestream[-1] = " + bin(bytestream[-3]))
        #send_to_COSMSOS(bytestream)
        logs_error_count = logs_error_count + 1
    
    logs_count = logs_count + 1
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
            elif bytestream[i] == 0x08 and bytestream[i+1] == 0x1E:
                decode_LOGS_pkt(bytestream[i:i+logs_pkt_len])
                i = i + logs_pkt_len
            elif bytestream[i] == 0x08 and bytestream[i+1] == 0x3C:
                decode_time_pkt(bytestream[i:i+time_pkt_len])
                i = i + time_pkt_len
            else:
                i = i + 1
            #i = i + 1
        else:
            break



def send_to_COSMSOS(bytestream):
    tx = str(bytestream)
    tx = tx.encode()
    tx = bytes(bytestream)
    HOST = "127.0.0.1"
    PORT = 27015
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.send(tx)
for fname in fnames:
    f = open(fname)
    c = f.readline()
    i = 0
    while 1:
        c = f.read(1)
        if c == 'A':
            print(i)
            dummy_bytes_1 = (i)/3 + 5
            dummy_bytes_1 = int(dummy_bytes_1)
            dummy_bytes_2 = int(59 - dummy_bytes_1)
            break
        i = i + 1
    c = f.readline()
    print("Db1 = " + str(dummy_bytes_1))
    print("Db2 = " + str(dummy_bytes_2))
    bytestream = []
    total = 0
    while 1:
        if dummy_bytes_1 != 0:
            c = f.read(dummy_bytes_1 * 3)
        c = f.read(1)
        if c == '':
            break
        c1 = int(str(c),16)
        c = f.read(1)
        if c == '':
            break
        c2 = int(str(c),16)
        byte_n = (c1 << 4) | c2
        bytestream.append(byte_n)
        total = total + 1
        if (total % 1000) == 0:
            print("Total = " + str(total))
        c = f.read(dummy_bytes_2 * 3 + 2)
        if c == '':
            break

    #send_to_COSMSOS(bytestream)
    separate_packets(bytestream)
    print("Total hk = " + str(hk_count))
    print("Error hk = " + str(hk_error))
    print("Total aris = " + str(aris_count))
    print("Error aris = " + str(aris_error))
    print("Total Thermistor = " + str(thermistor_count))
    print("Error Thermistor = " + str(thermistor_error_count))
    print("Total Logs = " + str(logs_count))
    print("Error Logs = " + str(logs_error_count))
    print("Sent to COSMOS")
    print("Db1 = " + str(dummy_bytes_1))
    print("Db2 = " + str(dummy_bytes_2))