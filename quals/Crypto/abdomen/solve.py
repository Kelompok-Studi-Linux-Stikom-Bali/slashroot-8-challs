from Crypto.Util.number import *
from pwn import * 
from functools import reduce

class RandomSequenceGenerator:
    def __init__(self, s):
        self._current_value = s

    def next(self, a, b, c):
        tmp = self._current_value * a
        adj = tmp + b
        self._current_value = divmod(adj, c)[1]
        return self._current_value

def genPrime(lcg, a, b, c):
    p = []
    prods = []
    
    hint = True

    it = 0
    shift = 10

    p_n = 1
    count = 0 

    while count < 10:
        cand = lcg.next(a,b,c)
        count += 1
        
        if 3 <= count <= 10:
            while True:
                if hint:
                    prods.append((cand << pow(2,shift)) + (cand >> (cand.bit_length() - shift)))
                    
                    it += 1
                    if it == 10:
                        hint = False
                if not isPrime(cand):
                    cand = lcg.next(a,b,c)
                else:
                    p_n *= cand
                    p.append(cand)
                    break
    
    return p

def crack_LCG(states, modulus=0, multiplier=0, increment=0):
    # crack modulus
    if modulus == 0:
        t = []
        for i in range(len(states) - 1):
            t.append(states[i+1] - states[i])
        u = []
        for i in range(len(t) - 2):
            result = abs(t[i+2] * t[i] - t[i+1]**2)
            u.append(result)
        modulus = reduce(GCD, u)

    # crack multiplier
    if multiplier == 0:
        multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus

    # crack increment
    if increment == 0:
        increment = (states[1] - states[0]*multiplier) % modulus

    return modulus, multiplier, increment

def connect():
    return remote('localhost', 10012)
    # return process('./chall.py', level='error')

def getN(conn):
    conn.recvuntil(b"n : ")
    n = int((conn.recvline().strip().decode()[2:]), 16)

    return n

def getFlag(conn):
    conn.sendline(b"1")
    conn.recvuntil(b"Your flag is : ")

    _enc = int((conn.recvline().strip().decode()[2:]), 16)

    conn.recvline()

    return _enc

def getStates(conn):
    conn.sendline(b"2")

    conn.recvuntil(b"Hint : ")

    truncated_s = [int(i) for i in conn.recvline().strip().decode()[1:-1].split(", ")]
    s = []

    for i in truncated_s:
        tmp = i - (i >> 2**10)
        si = i - tmp
        s.append(si)

    return s

def main():
    conn = connect()

    n = getN(conn)
    _enc = getFlag(conn)

    states = getStates(conn)
    seed = states[0]

    e = 65537

    c, a, b = crack_LCG(states)

    lcg = RandomSequenceGenerator(seed)

    primes = genPrime(lcg, a, b, c)

    phi = 1
    for i in primes:
        phi *= (i - 1)

    d = inverse(e, phi)

    m = long_to_bytes(pow(_enc,d,n))

    conn.sendline(b"3")
    conn.sendlineafter(b"Your Flag : ", m)

    status = conn.recvline().strip().decode()

    print(status)

    print(f"FLAG : {m.decode()}")


if __name__ == "__main__":
    main()