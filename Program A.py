# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 21:56:27 2025

@author: vijay
"""

import socket
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modInverse(A, M):
    if gcd(A, M) > 1:
        return -1
    X = 1
    while X < M:
        if ((A % M) * (X % M)) % M == 1:
            return X
        X += 1
    return -1

def affine_encrypt(text, a, b):
    encrypted = ""
    for i in range(len(text)):
        encrypted += " ".join(chr(((a * ord(text[i]) + b) % 128)))
    return encrypted

def otp_encrypt(plaintext, key):
    encrypted = ""
    for i in range(len(plaintext)):
        encrypted += " ".join(chr(ord(plaintext[i]) ^ ord(key[i])))
    return encrypted

with open('Putin1.dat', 'r') as file:
    plaintext = file.read()

    key = ""
    for items in range(len(plaintext)):
        key += chr(random.randint(0, 127))

    ciphertext = otp_encrypt(plaintext, key)
    file = open('Putin2.dat', 'w')
    for char in ciphertext:
        file.write(char)
    file.close()

    A, B = 5, 8
    encrypted_key = affine_encrypt(key, A, B)

    key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_socket.connect(('localhost', 2500))
    key_socket.send(encrypted_key.encode())
    key_socket.close()

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect(('localhost', 2501))
    data_socket.send(ciphertext.encode())
    data_socket.close()

    print("Program A: Encrypted key and data sent.")