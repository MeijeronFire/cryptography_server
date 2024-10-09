#!/usr/bin/env python3
import requests
import multiprocessing
import time
from datetime import datetime
from math import floor
from hashlib import sha256
from random import randint
import cryptils

###################################################################################################################
def message_preperation(msg_pre):
    msg_done = cryptils.decrypt_RSA(int(msg_pre)) # or: encrypt with private key
    msg_done = cryptils.encrypt_RSA(int(msg_done)) # or: encrypt with public key
    return msg_done


def generate_message(message_plain):
    now = datetime.now()  
    timestamp = datetime.timestamp(now)

    msg_hash = sha256(message_plain.encode('utf-8')).hexdigest()

    msg = message_preperation(message_plain)

    parameters = {
            "time": floor(timestamp),
            "hash": msg_hash,
            "msg": msg,
            "userID": userID
    }
    return parameters

def send(message_plain = "English or Spanish?"):
    parameters = generate_message(message_plain)
    r = requests.post(url="http://127.0.0.1:5000/send", data=parameters)
    #print(r.text)

def receive(current_msg = 0):
    r = requests.get(url="http://127.0.0.1:5000/receive", params={"current" : current_msg})
    return r.json()

###################################################################################################################

# array to store all data in
data_arr = []


# background data working
def update():
    while True:
        global data_arr
        latest_data = receive(len(data_arr))
        time.sleep(1)

        if latest_data != []:
            data_arr.extend(latest_data)
            for i in latest_data: 
                print(f"\n---------\n{i["userID"]}:\t{i["msg"]}\n---------\ncryptsystem01 ~$ ", end="")

    # multithreading boilerplate
    procname = multiprocessing.Process(target=func, name="proc 1")
    procname.daemon = True
    procname.start()
    procname.join()

# main loop / driver code
if __name__ == '__main__':

    # userID for identification purposes
    global userID
    userID = randint(0, 10000)

    # multithreading boilerplate
    procname = multiprocessing.Process(target=update, name="proc 1")
    procname.daemon = True
    procname.start()
    #procname.join()

    print("test")
    while True:
        inp = input("cryptsystem01 ~$ ")
        if inp == "q" or inp == "quit":
            exit()
        send(inp)

