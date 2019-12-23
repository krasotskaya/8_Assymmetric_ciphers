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

import socket
from time import sleep

sock = socket.socket()
sock.setblocking(1)
sock.connect(('10.38.205.43', 9090))
print('connection')
key_prim = 199
key_publ_m = 197
key_publ_s = 0
key_part_m = 0
key_part_s = 0
key_full_m = 0
key_full_s = 0
i = 0
msg = ''
while True:
    if i <= 3:
        i += 1
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
    else:
        msg = input()
        msg_new = coding(msg,key_full_m)
        sock.send(msg_new.encode())
        msg = sock.recv(1024).decode()
        msg_new = decoding(msg,key_full_m)
        print('m from server:\t', msg_new)
sock.close()