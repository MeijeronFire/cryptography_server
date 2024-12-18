#!/usr/bin/env python3

#from dotenv import load_dotenv
import os
import primes
from math import gcd
from random import randint
from dotenv import load_dotenv, set_key
from pathlib import Path

# .env prefab
env_path = Path(".env")
env_path.touch(mode=0o600, exist_ok=True)
load_dotenv()

primes.primeGen(100)

######################################
#                                    #
#   ███████    ████████     ██       #
#  ░██░░░░██  ██░░░░░░     ████      #
#  ░██   ░██ ░██          ██░░██     #
#  ░███████  ░█████████  ██  ░░██    #
#  ░██░░░██  ░░░░░░░░██ ██████████   #
#  ░██  ░░██        ░██░██░░░░░░██   #
#  ░██   ░░██ ████████ ░██     ░██   #
#  ░░     ░░ ░░░░░░░░  ░░      ░░    #
#                                    #
######################################

# Generate keys
def keygen_RSA():
    p1 = primes.primeGen(bits=2048)
    p2 = primes.primeGen(bits=2048)
    n = p1*p2
    set_key(dotenv_path=env_path, key_to_set="MOD_CLASS", value_to_set=str(n))

    phi = (p1-1)*(p2-1)

    while 1:
        e = randint(3, phi)
        if gcd(e, phi) == 1:
            break

    d = pow(e, -1, phi)

    set_key(dotenv_path=env_path, key_to_set="PUBKEY", value_to_set=str(e))
    set_key(dotenv_path=env_path, key_to_set="PRIVKEY", value_to_set=str(d))

# if the .env is _not_ present, generate it.
if not os.getenv("MOD_CLASS") or not os.getenv("PUBKEY") or not os.getenv("PRIVKEY"):
    keygen_RSA()

def to_int(ascii_str):
    values_pre = [ord(letter) for letter in ascii_str]
    values = [str(val).zfill(3) for val in values_pre]
    for i in values:
        ascii_int = int(''.join(map(str, values)))
    return ascii_int

def to_ascii(decr_int):
    values = []
    while decr_int>0: 
        remainder = decr_int%1000
        values.append(remainder)
        decr_int = decr_int//1000
    values.reverse()
    letters = [chr(ascii) for ascii in values]
    decr_msg = ''.join([str(ascii) for ascii in letters])
    return decr_msg

#Works for ascii now woo
def encrypt_RSA(message, base=int(os.getenv("PUBKEY")), modulo=int(os.getenv("MOD_CLASS"))):
    return pow(message, base, modulo)

# Works the same as encrypting with a private key.
def decrypt_RSA(message):
    base = int(os.getenv("PRIVKEY"))
    modulo = int(os.getenv("MOD_CLASS"))
    decr_int = pow(message, base, modulo)
    return decr_int


print("Succesfully initialized CrypTils v1.0!")
