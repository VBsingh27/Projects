# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 21:56:28 2025

@author: vijay
"""

import socket

def modInverse(A, M):
    for X in range(1, M):
        if (A * X) % M == 1:
            return X
    return -1

def affine_decrypt(text, a, b):
    a_inv = pow(a, -1, 128)
    decrypted = ""
    for i in range(len(text)):
        decrypted += chr(((a_inv * (ord(text[i]) - b)) % 128))
    return decrypted

def otp_decrypt(ciphertext, key):
    decrypted = ""
    for i in range(len(ciphertext)):
        decrypted += chr(ord(ciphertext[i]) ^ ord(key[i]))
    return decrypted

if __name__ == "__main__":
    key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_socket.bind(('localhost', 2500))
    key_socket.listen(1)
    conn, _ = key_socket.accept()
    encrypted_key = ""
    while True:
        chunk = conn.recv(1024).decode()
        if not chunk:
            break
        encrypted_key += chunk
    conn.close()
    key_socket.close()

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('localhost', 2501))
    data_socket.listen(1)
    conn, _ = data_socket.accept()
    ciphertext = ""
    while True:
        chunk = conn.recv(1024).decode()
        if not chunk:
            break
        ciphertext += chunk
    conn.close()
    data_socket.close()

    A, B = 5, 8
    key = affine_decrypt(encrypted_key, A, B)
    plaintext = otp_decrypt(ciphertext, key)

    outputFile = open('Putin2.dat', 'w')
    for char in plaintext:
        outputFile.write(char)
    outputFile.close()

    print("Decrypted message from Putin2.dat:")
    print(plaintext)