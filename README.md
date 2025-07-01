# secure_module Python
Security module which stores important and confidental information. Information is stored encrypted and password protected. The module also provides the WebEncr and WebDecr functions which encrypts and decrypts any object with AES-GCM 256-bit encryption. Have a look at SECURITY.md and read the information below for security informations.

# How to use the module
Have a look at the example.py file. Also know that you only need to copy the folder <i>secure_secrets_module</i> into your source code. Try to always keep the latest version in your code. New Versions will be named with semantic versioning https://semver.org/.
You need to have pycryptodomex installed. Example command for pip: pip install pycryptodomex.
<b>Keep aware always adding secrets without making a commit with the secret in plaintext!</b>
<b>Do not modify the secrets with the IDs Version and Key_AES</b>

## General information about AES-GCM
AES-GCM provides data integrity and confidentiality (it belongs to the class of authenticated encryption with associated data - AEAD algorithms).
For further information about GCM I recommend you to have a look at <i>http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf</i>. You can also have a look at <i>https://en.wikipedia.org/wiki/Galois/Counter_Mode</i>.

## Security
- For any given key, GCM is <b>limited to encrypting 2^39 - 256 bits of plain data (64GiB)</b>!
- It's security depends on a <b>unique nonce for every encryption performed with the same key</b>. Have a look at <i>http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf</i>.
- The authentication strength depends on the length of it's tag. The longer the tag (128 bit / 16 byte maximum) the better. 
- For information about Key Establishment have a look at section 8.1 in <i>http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf</i>.

## Information about my implementation

### nonce
I use a pseudo random nonce with 64 bytes length. If high security is needed or something like file encryption is wanted, I would recommend using a deterministic nonce, like described in section 8.2.1 in <i>http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf</i>. As the pycryptodomex implementation supports 16 byte nonces, I would use a 16 byte nonce. If you change the length of the nonce, the decrypt function must be adapted to the new length.
### authentication tag
I use the longest possible tag length, which ensures the highest possible authentication strength. Smaller tag lengths are highly discouraged.
### Key Generation
Generates a random key. For information about Key Establishment have a look at section 8.1 in <i>http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf</i>.
