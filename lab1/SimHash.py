import sys
import hashlib

def simhash(document):
    sh = [0 for i in range(128)]
    tokens = document.strip().split(" ")
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

# read data from stdin
input_data = sys.stdin.read().strip().split("\n")

# input text
N = int(input_data[0])
document_list = input_data[1:N+1]
assert(len(document_list) == N)

# input queries
Q = int(input_data[N+1])
query_list = input_data[N+2:]
assert(len(query_list) == Q)

# translate input text to simhashes
document_hash_list = list()
for document in document_list:
    document_hash_list.append(simhash(document))
assert(len(document_hash_list) == N)

def hamming_distance_threshold(hash1, hash2, K):
    # convert hex 1 to bits
    bits1 = bin(int(hash1, 16))[2:]
    bits1 = bits1.rjust(128, "0")
    # convert hex 2 to bits
    bits2 = bin(int(hash2, 16))[2:]
    bits2 = bits2.rjust(128, "0")
    # calculate hamming distance
    hamming_distance = 0
    for i, j in zip(bits1, bits2):
        if i != j:
            hamming_distance += 1
            if hamming_distance > K:
                return False
    if hamming_distance > K:
        return False
    else:
        return True

for query in query_list:
    I = int(query.split(" ")[0])
    K = int(query.split(" ")[1])
    document_hash = document_hash_list[I]
    similar_documents = 0
    for compare_hash in document_hash_list:
        if hamming_distance_threshold(document_hash, compare_hash, K):
            similar_documents += 1
    # don't count itself
    similar_documents -= 1
    print(similar_documents)
