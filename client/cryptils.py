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
def keygen():
    p1 = primes.primeGen()
    p2 = primes.primeGen()
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

def encrypt(message):
    base = int(os.getenv("PUBKEY"))
    modulo = int(os.getenv("MOD_CLASS"))
    return pow(message, base, modulo)

def decrypt(message):
    base = int(os.getenv("PRIVKEY"))
    modulo = int(os.getenv("MOD_CLASS"))
    return pow(message, base, modulo)

# if the .env is _not_ present, generate it.
if not os.getenv("MOD_CLASS") or not os.getenv("PUBKEY") or not os.getenv("PRIVKEY"):
    keygen()

print("Succesfully initialized CrypTils v1.0!")
