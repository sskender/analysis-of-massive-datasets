import sys
import hashlib

# read data from stdin
input_data = sys.stdin.read().strip().split("\n")

def simhash(text):
    sh = [0 for i in range(128)]
    tokens = text.strip().split(" ")
    for token in tokens:
        hashed = hashlib.md5(token.encode())
        result = hashed.hexdigest()
        bits = bin(int(result, 16))[2:]  # remove 0b prefix
        bits = bits.rjust(128, "0")  # fix padding
        for i in range(len(bits)):
            if bits[i] == "1":
                sh[i] += 1
            else:
                sh[i] -= 1
    for i in range(len(sh)):
        if sh[i] >= 0:
            sh[i] = 1
        else:
            sh[i] = 0
    hex_result = hex(int("".join(map(str, sh)), 2))[2:]  # remove 0x prefix
    return hex_result.rjust(32, "0")  # fix padding

# validate simhash function
test_in = "fakultet elektrotehnike i racunarstva"
test_out = "f27c6b49c8fcec47ebeef2de783eaf57"
assert(simhash(test_in) == test_out)

# input text
N = int(input_data[0])
text_list = input_data[1:N+1]
assert(len(text_list) == N)

# input queries
Q = int(input_data[N+1])
Q_list = input_data[N+2:]
assert(len(Q_list) == Q)
