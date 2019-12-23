# -*- coding: utf-8 -*-

"""

Created on Tue Dec 17 15:55:48 2019



@author: Елизавета

"""



#server



def calc_part_key(key_publ_s, key_prim, key_publ_m):
    key_part_m = key_publ_s ** key_prim % key_publ_m
    return key_part_m

def calc_full_key(key_part_s, key_prim, key_publ_m):
    key_full = key_part_s ** key_prim % key_publ_m
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
            key_publ_s = int(conn.recv(1024))
            msg = str(key_publ_m)
            conn.send(msg.encode())
    if i == 2:
            key_part_s = int(conn.recv(1024))
            key_part_m = calc_part_key(key_publ_s, key_prim, key_publ_m)
            msg = str(key_part_m)
            conn.send(msg.encode())
    if i == 3:
            key_full_s = int(conn.recv(1024))
            key_full_m = calc_full_key(key_part_s, key_prim, key_publ_m)
            msg = str(key_full_m)
            conn.send(msg.encode())
            print(key_full_s)
            with open ('keys_s.txt','w') as f:
                f.write(str(key_full_m))
    
def mess(conn, key_full_m):
    msg = conn.recv(1024).decode()
    msg_new = decoding(msg,key_full_m)
    print('m from server:\t', msg_new)
    msg = input('m from you:\t')
    msg_new = coding(msg,key_full_m)
    conn.send(msg_new.encode())
    
def check(key_publ_s):
    i = False
    with open ('key_list.txt', 'r') as f:
        for line in f:
            if line == str(key_publ_s):
                i = True
    return i

import socket
sock = socket.socket()
sock.bind(('', 9090))
print('connection')
sock.listen(3)
i = 0
conn, addr = sock.accept()
print(addr)
try:
    with open ('keys_s.txt','r') as f:
        for line in f:
            key_full_m = int(line);
except:
    key_publ_m = 151
    key_prim = 157
    i = 0
    msg = ''
    while i<3:
        i += 1
        gener(i, key_prim, key_publ_m)
while True:
    mess(conn, key_full_m)

conn.close()