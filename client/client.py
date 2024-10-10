#!/usr/bin/env python3
import requests
import os
import multiprocessing
import time
from datetime import datetime
from math import floor
from hashlib import sha256
from random import randint
import cryptils
from pathlib import Path
from funcy import join

# .env prefab

###################################################################################################################

def validate_integrity(msg_plain, hash_signed, senderID):
    user_dict = {}
    for d in ns.user_arr:
        user_dict.update(d)
    sender_pubk = user_dict[str(senderID)][0]
    sender_modc = user_dict[str(senderID)][1]
    suspected_hash = int.from_bytes(sha256(msg_plain.encode('utf-8')).digest(), 'big')
    # de - signed, as in, removed the sign.
    hash_designed = cryptils.encrypt_RSA(int(hash_signed), base=sender_pubk, modulo=sender_modc)
    if hash_designed == suspected_hash:
        return True
    return False

def message_postprocessing(msg_pre, alleged_senderID): 
    # the user_arr looks like: [{...:[...]}, {...:[...]}, {...:[...]}] etc. We convert it to {...:[...], ...:[...], ...:[...]}.
    user_dict = {}
    for d in ns.user_arr:
        user_dict.update(d)
    a_sender_pubk = user_dict[str(alleged_senderID)][0]
    a_sender_modc = user_dict[str(alleged_senderID)][1]
    msg_decrypted = cryptils.decrypt_RSA(msg_pre) 
    #msg_designed = cryptils.encrypt_RSA(msg_decrypted, base=a_sender_pubk, modulo=a_sender_modc)
    #msg_designed = cryptils.encrypt_RSA(msg_pre, base=a_sender_pubk, modulo=a_sender_modc)

    #return msg_designed
    return msg_decrypted


def generate_message(message_plain, target_pubk, target_modc):
    now = datetime.now()  
    timestamp = datetime.timestamp(now)

    msg_hash = int.from_bytes(sha256(message_plain.encode('utf-8')).digest(), 'big')
    signed_msg_hash = cryptils.decrypt_RSA(msg_hash) # the same as signing :wow:

    msg_done = cryptils.encrypt_RSA(int(message_plain), base=target_pubk, modulo=target_modc) # or: encrypt with public key

    parameters = {
            "time": floor(timestamp),
            "hash": signed_msg_hash,
            "msg": msg_done,
            "userID": userID
    }
    return parameters

def send(message_plain, target_id):
    #global user_arr

    # the user_arr looks like: [{...:[...]}, {...:[...]}, {...:[...]}] etc. We convert it to {...:[...], ...:[...], ...:[...]}.
    user_dict = {}
    for d in ns.user_arr:
        user_dict.update(d)
    target_pubk = user_dict[target_id][0]
    target_modc = user_dict[target_id][1]
    parameters = generate_message(message_plain, target_pubk, target_modc)
    r = requests.post(url="http://127.0.0.1:5000/send", json=parameters)

def receive(current_msg = 0):
    r = requests.get(url="http://127.0.0.1:5000/receive", params={"current" : current_msg})
    return r.json()

###################################################################################################################

# background data working
def update():
    data_arr = []
    while True:
        ns.user_arr = requests.get(url="http://localhost:5000/getusers").json()
        latest_data = receive(len(data_arr))
        time.sleep(1)

        if latest_data != []:
            data_arr.extend(latest_data)
            for i in latest_data:
                msg_plain = message_postprocessing(i["msg"], i["userID"])
                if validate_integrity(str(msg_plain), i["hash"], i["userID"]):
                    print("\n---\nintegrity validated\n---")
                    print(f"\n---------\n{i["userID"]}:\t{msg_plain}\n---------\ncryptsystem01 ~$ ", end="")

    # multithreading boilerplate
    procname = multiprocessing.Process(target=func, name="proc 1")
    procname.daemon = True
    procname.start()
    procname.join()

##################################################################################################################

# main loop / driver code
if __name__ == '__main__':

    # userID for identification purposes
    global userID
    userID = randint(0, 10000)

    # connect and register to server
    register_info = {
            userID: [
                int(os.getenv("PUBKEY")), 
                int(os.getenv("MOD_CLASS"))
            ]
    }
    requests.post(url="http://localhost:5000/register", json=register_info)

    # Allowing objects to be shared between threads
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.user_arr = []

    # multithreading boilerplate
    procname = multiprocessing.Process(target=update, name="proc 1")
    procname.daemon = True
    procname.start()
    #procname.join()

    print(userID)
    while True:
        inp = input("cryptsystem01 ~$ ")
        if inp == "q" or inp == "quit":
            exit()
        tokenized_inp = inp.split(" ")
        print(tokenized_inp)
        send(tokenized_inp[1], tokenized_inp[0])

