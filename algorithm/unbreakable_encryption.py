from secrets import token_bytes
from typing import Tuple

def random_key(length: int):
    # create length of random-bytes
    tb: bytes = token_bytes(length)
    # convert this bytes in a bit-string and return
    print("tb: ", tb)
    return int.from_bytes(tb, "big")

def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    print("original", bin(original_key))
    encrypted: int = original_key ^ dummy # XOR
    return dummy, encrypted

def decrypt(key1: int, key2: int):
    decrypted: int = key1 ^ key2
    print("key1: ", bin(key1))
    print("key2: ", bin(key2))
    print("decrypted: ", bin(decrypted))
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    print(decrypted.bit_length())
    return temp.decode()

if __name__ == "__main__":
    key1, key2 = encrypt("chess is dumb")
    result: str = decrypt(key1, key2)
    print(result)