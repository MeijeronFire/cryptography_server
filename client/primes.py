#!/usr/bin/env python3
import math
from gmpy2 import powmod
from random import randint
import time

def isDiv(num, div):
    return (num // div) * div == num

def isOdd(num):
    return (num % 2 == 1)

def twoSD(num):
    i = 1
    D = (num-1) // 2
    while not isOdd(D):
        D //= 2
        i+=1

    S = i
    ##print(num, (2**S)*D+1)
    #print(num, S, D)
    return (int(S), int(D))

def sieveCheck(num, trials=25):
    primeTable = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    for i in range(0, trials):
        if isDiv(num, primeTable[i]):
            return False
    return True

def isPrime(num, iterations=64, trials=25):
    if not sieveCheck(num, trials=25):
        return False
    for i in range(0, iterations):
        #print(i)
        a = randint(2, num - 2) # generate A
        num_rewrite = twoSD(num)
        y = powmod(a, num_rewrite[1], num)
        #print(y)
        if y != 1 and y != num-1:
            j = 1
            while j <= (num_rewrite[0]-1) and y != num-1:
                #print(j)
                y = pow(y, 2, num)
                #print(y)
                if y == 1:
                    #if i != 0: print(i)
                    return False
                j = j+1
            if y != num-1:
                #if i != 0: print(i)
                return False
    #print(i)
    return True

def primeGen(bits=256, iterations=128, trials=25):
    #print(twoSD(48112959837082048697))
    found = False
    while not found:
        prime_candidate = randint(3, pow(2, bits-1))*2-1
        found = isPrime(prime_candidate, trials=25)
        #print("uh")
    return prime_candidate

#print(primeGen(2048, iterations = 256, trials = 150))
