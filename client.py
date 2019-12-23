# -*- coding: utf-8 -*-

"""

Created on Tue Dec 17 16:00:08 2019



@author: Елизавета

"""



#client



def calc_part_key(key_publ_m, key_prim, key_publ_s):
    key_part_m = key_publ_m ** key_prim % key_publ_s
    return key_part_m


def calc_full_key(key_part_s, key_prim, key_publ_s):
    key_full = key_part_s ** key_prim % key_publ_s
    return key_full



def coding (st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j += key
        j = chr(j)
        s[i] = j
    return(''.join(s))


def decoding (st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j -= key
        j = chr(j)
        s[i] = j
    return(''.join(s))

def gener(i, key_prim, key_publ_m):
    if i == 1:
            msg = str(key_publ_m)
            sock.send(msg.encode())
            key_publ_s = int(sock.recv(1024))
    if i == 2:
            key_part_m = calc_part_key(key_publ_m, key_prim, key_publ_s) 
            msg = str(key_part_m)
            sock.send(msg.encode())
            key_part_s = int(sock.recv(1024))
    if i == 3:
            key_full_m = calc_full_key(key_part_s, key_prim, key_publ_s)
            print(key_part_s, key_prim, key_publ_s)
            msg = str(key_full_m)
            sock.send(msg.encode())
            key_full_s = int(sock.recv(1024))
            print(key_full_s)
            with open ('keys_c.txt','w') as f:
                f.write(str(key_full_s))
                
def mess(sock, key_full_m):
    msg = input('m from you:\t')
    msg_new = coding(msg,key_full_m)
    sock.send(msg_new.encode())
    msg = sock.recv(1024).decode()
    msg_new = decoding(msg,key_full_m)
    print('m from server:\t', msg_new)
        
import socket
sock = socket.socket()
sock.setblocking(1)
sock.connect(('localhost', 9090))
print('connection')
try:
    with open ('keys_c.txt','r') as f:
        for line in f:
            key_full_m = int(line);
except:
    key_prim = 199
    key_publ_m = 197
    i = 0
    msg = ''

    while i<3:
        i += 1
        gener(i, key_prim, key_publ_m)
while True:    
    mess(sock, key_full_m)

sock.close()
