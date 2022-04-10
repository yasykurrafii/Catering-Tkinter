from Crypto.Hash import SHA256

def encrypt(data : str):
    hashing = SHA256.new()
    hashing.update(data.encode('utf-8'))
    return hashing.hexdigest()