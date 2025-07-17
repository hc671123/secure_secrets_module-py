from Cryptodome.Cipher import AES  #you need  to install pycryptodomex (example: pip install pycryptodomex)
import secrets

def encrypt(plaindata: bytes, key: bytes, data_to_auth: bytes | None = None, nonce: bytes | None = None) -> bytes:
    if nonce == None:
        nonce = secrets.token_bytes(64) #look at README.md for more information about the nonce and it's security flaws
    aes = AES.new(key,AES.MODE_GCM, nonce=nonce, mac_len=16) #instantiates a new GCM cipher object for AES - have a look at README.md
    if data_to_auth != None:
        aes.update(data_to_auth)#If wanted data which shall not be encrypted but it's data integrity should be ensured can be added
    cipherdata, tag = aes.encrypt_and_digest(plaindata)
    return nonce+tag+cipherdata #returns the tag, nonce and cipherdata
    
def decrypt(cypherdata: bytes, key: bytes, data_to_auth: bytes | None= None) -> bytes:
    #splits the cypherdata in its components
    #if the nonce  or tag length is changed, the following split values must be adapted
    nonce = cypherdata[0:64] 
    tag = cypherdata[64:80]
    data = cypherdata[80:]
    aes = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16) 
    if data_to_auth != None:
        aes.update(data_to_auth)
    plaindata = aes.decrypt_and_verify(data, tag) #raises a ValueError if the MAC check fails (if the data was tampered with)
    return plaindata

def random_key(length_in_bits: int = 256) -> bytes:
    key = secrets.randbits(length_in_bits).to_bytes(32,'little')
    return key