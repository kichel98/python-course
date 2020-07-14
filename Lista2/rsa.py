import math
import argparse
import secrets
import random
import textwrap


def set_parser():
    parser = argparse.ArgumentParser(description="RSA Encryption/Decryption")
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--gen-keys", help="Generating public and private keys, require number of bits", type=int)
    action_group.add_argument("--encrypt", help="Encryption using key.pub")
    action_group.add_argument("--decrypt", help="Decryption using key.prv")

    return parser


def is_prime_miller(n, k=40):
    if n % 2 == 0:
        return False

    r = 1
    while (n-1) % pow(2, r+1) == 0:
        r += 1
    d = (n - 1) // pow(2, r)

    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    else:
        return True


def get_random_prime(prime_length):
    max_val = 10**prime_length  # exclusive
    min_val = 10**(prime_length - 1)  # inclusive

    rand = secrets.randbelow(max_val - min_val) + min_val
    while not is_prime_miller(rand):
        rand = secrets.randbelow(max_val - min_val) + min_val
    return rand


def get_random_prime_pair(prime_length):
    p = get_random_prime(prime_length)
    q = get_random_prime(prime_length)
    while p == q:
        q = get_random_prime(prime_length)
    n = p * q
    phi = (p - 1)*(q - 1)
    return p, q, n, phi


def extended_euclid(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1
    while a % b != 0:
        q = a // b
        a, b, x1, y1, x2, y2 = b, a % b, x2, y2, x1 - q*x2, y1 - q*y2
    # return b, x2, y2
    return x2  # we only need x2


def write_to_file(filename, data_list):
    with open(filename, "w") as f:
        for data in data_list:
            f.write(str(data))
            f.write(" ")


def read_from_file(filename):
    with open(filename, "r") as f:
        return f.read().split()


def generate_keys(bits, pub_key_path, prv_key_path):
    e = 65537
    prime_length = int(math.log(2, 10) * bits)

    p, q, n, phi = get_random_prime_pair(prime_length)
    while math.gcd(phi, e) != 1:
        p, q, n, phi = get_random_prime_pair(prime_length)
    d = extended_euclid(e, phi)
    if d < 0:
        d += phi

    write_to_file(pub_key_path, [n, e])
    write_to_file(prv_key_path, [n, d])


def encrypt(plain_text, pub_key_path):
    letter_codes = ["{0:x}".format(ord(char)) for char in plain_text]
    try:
        pub_key = read_from_file(pub_key_path)
    except FileNotFoundError:
        print("Cannot find public key. You need to generate keys first, check:\n\tpython rsa.py --help\n")
        raise

    n = int(pub_key[0])
    e = int(pub_key[1])
    return pow(int("".join(letter_codes), base=16), e, n)


def decrypt(enc_data, prv_key_path):
    try:
        prv_key = read_from_file(prv_key_path)
    except FileNotFoundError:
        print("Cannot find private key. You need to generate keys first, check:\n\tpython rsa.py --help\n")
        raise

    n = int(prv_key[0])
    d = int(prv_key[1])
    decimal_val = pow(int(enc_data), d, n)
    letter_codes = textwrap.wrap("{0:x}".format(decimal_val), 2)

    return "".join(list(map(lambda code: bytes.fromhex(code).decode(), letter_codes)))


def rsa():
    pub_key_path = "key.pub"
    prv_key_path = "key.prv"
    parser = set_parser()
    args = parser.parse_args()
    if args.gen_keys is not None:
        generate_keys(args.gen_keys, pub_key_path, prv_key_path)
    elif args.encrypt is not None:
        print(encrypt(args.encrypt, pub_key_path))
    elif args.decrypt is not None:
        print(decrypt(args.decrypt, prv_key_path))


rsa()
