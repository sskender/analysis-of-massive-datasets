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
        for i, bit in enumerate(bits):
            if bit == "1":
                sh[i] += 1
            else:
                sh[i] -= 1
    for i in range(128):
        if sh[i] >= 0:
            sh[i] = 1
        else:
            sh[i] = 0
    hex_result = hex(int("".join(map(str, sh)), 2))[2:]  # remove 0x prefix
    return hex_result.rjust(32, "0")  # fix padding

def create_lsh_buckets(document_hash_list, b=8):
    candidates = {}
    band_size = 128 // b
    for i in range(0, 128, band_size):
        buckets = {}
        for document_id in range(len(document_hash_list)):
            document_hash = document_hash_list[document_id]
            bits = bin(int(document_hash, 16))[2:]
            bits = bits.rjust(128, "0")
            band_bits = bits[i:i+band_size]
            band_int = int(band_bits, 2)
            bucket_documents = set()
            if band_int in buckets:
                bucket_documents = buckets[band_int]
                for bucket_document_id in bucket_documents:
                    if document_id not in candidates:
                        candidates[document_id] = set([bucket_document_id])
                    else:
                        candidates[document_id].add(bucket_document_id)
                    if bucket_document_id not in candidates:
                        candidates[bucket_document_id] = set([document_id])
                    else:
                        candidates[bucket_document_id].add(document_id)
            bucket_documents.add(document_id)
            buckets[band_int] = bucket_documents
    return candidates

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
    return True

# input documents and hash them in the same pass
N = int(sys.stdin.readline().strip())
document_hash_list = []
for i in range(N):
    document = sys.stdin.readline().strip()
    document_hash_list.append(simhash(document))

# create buckets of similar documents
similar_candidates = create_lsh_buckets(document_hash_list)

# input queries and execute them in the same pass
Q = int(sys.stdin.readline().strip())
for i in range(Q):
    query = sys.stdin.readline().strip()
    I = int(query.split(" ")[0])
    K = int(query.split(" ")[1])
    if I in similar_candidates:
        document_hash = document_hash_list[I]
        candidates_list = similar_candidates[I]
        similar_documents = 0
        for candidate_id in candidates_list:
            compare_hash = document_hash_list[candidate_id]
            if hamming_distance_threshold(document_hash, compare_hash, K):
                similar_documents += 1
        print(similar_documents)
    else:
        print(0)
