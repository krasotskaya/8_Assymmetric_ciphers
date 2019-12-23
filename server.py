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

import socket

sock = socket.socket()
sock.bind(('', 9090))
print('connection')
sock.listen(3)
i = 0
conn, addr = sock.accept()
print(addr)
key_publ_m = 151
key_prim = 157
key_publ_s = 0
key_part_m = 0
key_part_s = 0
key_full_m = 0
key_full_s = 0
msg = ''
while i != 3:
    i += 1
    if i == 1:
        key_publ_s = int(conn.recv(1024))
        msg = str(key_publ_m)
        conn.send(msg.encode())
        print(key_publ_s)
    if i == 2:
        key_part_s = int(conn.recv(1024))
        key_part_m = calc_part_key(key_publ_s, key_prim, key_publ_m)
        msg = str(key_part_m)
        conn.send(msg.encode())
        print(key_part_s)
    if i == 3:
        key_full_s = int(conn.recv(1024))
        key_full_m = calc_full_key(key_part_s, key_prim, key_publ_m)
        msg = str(key_full_m)
        conn.send(msg.encode())
        print(key_full_s)
    	
conn.close()