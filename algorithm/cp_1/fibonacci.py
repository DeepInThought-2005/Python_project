from typing import Dict
# from functools import Iru_cache

fib2_counter = 0
fib3_counter = 0
fib4_counter = 0
fib5_counter = 0
fib6_counter = 0



def fib2(n: int) -> int:
    global fib2_counter
    fib2_counter += 1
    if n < 2: return n
    return fib2(n - 1) + fib2(n - 2)

memo: Dict[int, int] = {0: 0, 1: 1}

def fib3(n: int) -> int:
    global fib3_counter
    fib3_counter += 1
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2) # memoisation
    return memo[n]

'''
#alternative
@Iru_cache(maxsize=None)
def fib4(n: int) -> int:
    global fib4_counter
    fib4_counter += 1
    if n < 2: return n
    return fib4(n - 1) + fib4(n - 2)
'''

def fib5(n : int) -> int:
    global fib5_counter
    fibo1 = 0
    fibo2 = 1
    result = 0
    for _ in range(1, n):
        fib5_counter += 1
        result = fibo1 + fibo2
        fibo1 = fibo2
        fibo2 = result
        '''
        # alternative
        fibo1, fibo2 = fibo2, fibo1 + fibo2
        '''

    return result

def fib6(n : int) -> int:
    global fib6_counter
    fibo1 = 0
    fibo2 = 1
    result = 0
    for _ in range(1, n):
        fib6_counter += 1
        result = fibo1 + fibo2
        fibo1 = fibo2
        fibo2 = result
        '''
        # alternative
        fibo1, fibo2 = fibo2, fibo1 + fibo2
        '''
        yield result

    yield result

if __name__ == "__main__":
    print(str(fib2(5)) + " with " + str(fib2_counter) + " calls")
    print(str(fib3(50)) + " with " + str(fib3_counter) + " calls")
    print(str(fib5(50)) + " with " + str(fib5_counter) + " calls")
    for i in fib6(50):
        print(str(i) + " with " + str(fib6_counter) + " calls")
