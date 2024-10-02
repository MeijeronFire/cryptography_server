from random import randint
import time
import primes
start_time = time.time()

def fast_is_prime(p,accuracy=64):
    if p == 1:
        return False
    return all(pow(randint(1,p-1), p-1, p) == 1 for i in range(accuracy))

p = 6
total_primes = 0
prime_need = 100000
while total_primes < prime_need:
    p = randint(5*10**99, 5*10**100)*2+1
    if fast_is_prime(p,accuracy=64) is True:
        #print(p, "is prime")
        if not primes.isPrime(p):
            print(f"{p} is NOT PRIME HAHAA")
        total_primes += 1
total_time = time.time() - start_time
speed = prime_need/total_time
print(speed, "primes per second")
