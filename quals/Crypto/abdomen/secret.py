from sympy import isprime, nextprime, gcd, randprime, primerange
from Crypto.Util.number import getPrime
import random

def generate_state():
    c = getPrime(512)
    
    phi = c - 1
    
    a = random.randint(1<<29, c)
    while gcd(a, phi) != 1 or not isprime(a):
        a = nextprime(a)
    
    b = randprime(1<<29, c)
    
    state = randprime(1<<29, c)
    
    return c, a, b, state

flag = b"slashroot8{n3ith3r_3asy_nor_hard_ch4ll_for_crypt0_ch4ll}"  

c,a,b,state = generate_state()