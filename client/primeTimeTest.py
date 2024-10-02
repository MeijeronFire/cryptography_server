#!/usr/bin/env python3
import primes
import time
import os
#print(primes.sieveCheck(113))

# Measure _three_ parameters: M.-B. iterations, bit size and sieve checks. All over time

# so output is like this:
# [bit size] [# MB iterations] [# sieve chekcs] [time in primes per second]

#primes.primeGen(128, 64, 0)
#print("yh")

start = time.time()
for i in range(0, 1000):
    primes.primeGen(128, 64, 46)
end = time.time()
print(f"{1000/(end-start)}")

exit()

# bit size
def bitSize():
    for i in range(128, 516, 1):
        start = time.time()
        for j in range(0, 10000):
            bits = i 
            its = 64
            checks = 0
            primes.primeGen(bits, its, checks)
            #print(j)
        end = time.time()
        print(f"{bits}\t{its}\t{checks}\t{10000/(end-start)}")

#exit()

# # of MB iterations
def MBIterations():
    for i in range(0, 2000, 1000):
        start = time.time()
        for j in range(0, 100000):
            bits = 128
            its = i
            checks = 0
            primes.primeGen(bits, its, checks)
        end = time.time()
        print(f"{bits}\t{its}\t{checks}\t{(end-start)/100000}")

# # of sieve checks
def sieveChecks():
    for i in range(0, 2000, 1000):
        start = time.time()
        for j in range(0, 10000):
            bits = 128
            its = 64
            checks = i
            primes.primeGen(bits, its, checks)
        end = time.time()
        print(f"{bits}\t{its}\t{checks}\t{(end-start)/10000}")

MBIterations()
exit()

###############################################################33333
# # of sieve checks (with bigger bits)
for i in range(0, 168):
    start = time.time()
    for j in range(0, 1000):
        bits = 256
        its = 64
        checks = i
        primes.primeGen(bits, its, checks)
    end = time.time()
    print(f"{bits}\t{its}\t{checks}\t{1000/(end-start)}")

# # of sieve checks (with more its)
for i in range(0, 168):
    start = time.time()
    for j in range(0, 1000):
        bits = 128
        its = 128
        checks = i
        primes.primeGen(bits, its, checks)
    end = time.time()
    print(f"{bits}\t{its}\t{checks}\t{1000/(end-start)}")

# # of sieve checks (with more of both)
for i in range(0, 168):
    start = time.time()
    for j in range(0, 1000):
        bits = 256
        its = 128
        checks = i
        primes.primeGen(bits, its, checks)
    end = time.time()
    print(f"{bits}\t{its}\t{checks}\t{1000/(end-start)}")
