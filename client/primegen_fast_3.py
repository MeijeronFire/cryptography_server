from random import randint
from gmpy2 import powmod
import time
start_time = time.time()

#Setting up some functions
def isdiv(p,i):
	if p%i == 0:
		return True
	else:
		return False

def SieveCheck(p):
	sieve_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
	for i in sieve_primes:
		if isdiv(p,i) == True:
			return True
			break
	else:
		return False

#Actual Miller-Rabin test found here
def fast_is_prime(p,accuracy=64):
	#if p == 1:
		#return False
	return all(powmod(randint(1,p-1), p-1, p) == 1 for i in range(accuracy))

#Magic happens here
#total_primes = 0
#prime_need = 1000
#while total_primes < prime_need:
#	p = randint(1, 2**127)*2+1
#	if SieveCheck(p) == False:
#		if fast_is_prime(p,accuracy=64) is True:
#			#print(p)
#			total_primes += 1

#Timekeeping for benchmarking's sake
#total_time = time.time() - start_time
#speed = prime_need/total_time
#print(speed, "primes per second")
