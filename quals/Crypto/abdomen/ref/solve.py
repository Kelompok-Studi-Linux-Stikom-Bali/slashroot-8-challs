import os
os.environ['PWNLIB_NOTERM'] = 'True'
from pwn import process, remote
from sage.all import matrix, vector, RR, ZZ, floor

def connect():
    # return remote('0.0.0.0', 1337)
    return process('./chall.py', level='error')

def recv(conn):
    o = conn.recvline().decode()
    print('[<]', o)
    return o

def send(conn, data):
    print('[>]', data)
    conn.sendline(data)

def do_round(conn, trunc, guess=[1337]):
    recv(conn)
    send(conn, ' '.join(str(x) for x in guess))
    r = recv(conn)
    num = int(r.split('was ')[1])
    w = num % 2**trunc
    z = (num >> trunc) % 2**trunc
    return w, z

def get_params(conn):
    M = ZZ(recv(conn).split('M = ')[1])
    a = ZZ(recv(conn).split('a = ')[1])
    c = ZZ(recv(conn).split('c = ')[1])
    return M, a

def get_next_lcg_outputs(xprime, wk, zk, a, M, trunc):
    def r(xp):
        zk_next = (xp + zk) % 2**trunc
        wk_next = ((xp >> (M.nbits() - trunc)) + wk) % 2**trunc
        return (zk_next << trunc) + wk_next

    outputs = []

    xp = (a*xprime)%M
    outputs.append(r(xp))
    outputs.append(r(xp - M))
    outputs.append(r(xp) + 1)
    outputs.append(r(xp - M) + 1)

    return outputs

def recover_Xprime(W, Z, a, M, trunc):
    k = len(Z)-1

    Wprime = [W[i+1] - W[i] for i in range(k)]
    Zprime = [Z[i+1] - Z[i] for i in range(k)]
    
    L = [[a**i] + [0]*(i-1) + [-1] + [0]*(k-1-i) for i in range(1, k)]

    L.insert(0, [M] + [0]*(k-1))

    L = matrix(L)

    B = L.LLL()

    P1 = 2**(M.nbits() - trunc) * B * vector(Wprime) + B * vector(Zprime)
    P2 = vector([((RR(p) / M).round() * M - p)/(2**trunc) for p in P1])

    Yprime = list(B.solve_right(P2))
    Xprime = [2**(M.nbits() - trunc)*Wprime[i] + (2**trunc * Yprime[i]) + Zprime[i] for i in range(k)]
    return list(map(ZZ, Xprime))

def play_game():
    conn = connect()
    recv(conn)
    recv(conn)
    M, a = get_params(conn)
    
    trunc = 20

    WZ = [do_round(conn, trunc), do_round(conn, trunc)]

    W = [wz[0] for wz in WZ]
    Z = [wz[1] for wz in WZ]


    Xprime = recover_Xprime(W, Z, a, M, trunc)

    for _ in range(23-2):
        w, z = do_round(conn, trunc, get_next_lcg_outputs(Xprime[-1], W[-1], Z[-1], a, M, trunc))
        W.append(w)
        Z.append(z)
        Xprime = recover_Xprime(W, Z, a, M, trunc)
        print(Xprime)

    recv(conn)

play_game()