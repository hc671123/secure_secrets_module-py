import json
from . import AES_GCM
import base64
from .files import backendpath

class secrets:
    """Security module which stores important and confidental information.
    Information is stored encrypted and password protected. 
    The module also provides the WebEncr and WebDecr functions which encrypts and decrypts any object with AES-GCM 256-bit encryption.
    """
    def __init__(self, password: str = None):
        #change this variable for faster hashing (lower the number) or more secure hashing (raise the number). A value below 1000000 is highly discouraged.
        self.iterations_pbkdf_hashing = 10_000_000
        
        import getpass
        from os import path
        
        if password == None:
            password = getpass.getpass('Type in your encryption password -->')
            
        if not path.exists(backendpath('data.secrets')):
            print('initializing secure_module')
            self.__init_secure_module(password)
        
        with open(backendpath('s.bin'),'rb') as f:
            salt = f.read(128) 
        
        from hashlib import pbkdf2_hmac
        password_key = pbkdf2_hmac('sha-256',password.encode('utf-8'), salt, self.iterations_pbkdf_hashing)
        
        with open(backendpath('k.bin'),'rb') as f:
            secure_module_key_encrypted = f.read()
            
        self.secure_module_key = AES_GCM.decrypt(secure_module_key_encrypted,password_key)        
        self.__load_secrets()
    
    def __load_secrets(self) -> None:
        with open(backendpath('data.secrets'),'rb') as f:
            self.secrets = f.read()
        self.secrets = AES_GCM.decrypt(self.secrets,self.secure_module_key).decode('utf-8')
        self.secrets: dict = json.loads(self.secrets)
        self.aeskey = self.secrets['Key_AES']['data']
        self.aeskey = base64.b64decode(self.aeskey)
        
    def add_secret(self, id: str, data) -> None:
        
        #handling of binary data
        if type(data)==type(b'12'):
            binary = True
            data = base64.b64encode(data).decode('ascii')
        else:
            binary = False
            
        self.secrets.update({id: {'data': data,'binary': binary, 'private': False}})
        secr = json.dumps(self.secrets).encode('utf-8')
        secr = AES_GCM.encrypt(secr, self.secure_module_key)
        with open(backendpath('data.secrets'),'wb') as f:
            f.write(secr)
    
    def get_secret(self, id: str):
        secret = self.secrets[id]
        data = secret['data']
        
        #handling of binary data
        if secret['binary']:
            data = base64.b64decode(data)
            
        return data
    
    def password_change(self) -> None:
        import getpass
        #Checking if old password is valid
        password = getpass.getpass('enter your current password -->')
        with open(backendpath('s.bin'),'rb') as f:
            salt = f.read(128) 
        from hashlib import pbkdf2_hmac
        password_key = pbkdf2_hmac('sha-256',password.encode('utf-8'), salt, self.iterations_pbkdf_hashing)
        with open(backendpath('k.bin'),'rb') as f:
            secure_module_key_encrypted = f.read()
        self.secure_module_key = AES_GCM.decrypt(secure_module_key_encrypted,password_key) 
        
        #changes to new password
        password = getpass.getpass('enter the new encryption password -->')
        from os import urandom
        salt = urandom(128)
        with open(backendpath('s.bin'),'wb') as f:
            f.write(salt)
        
        from hashlib import pbkdf2_hmac
        password_key = pbkdf2_hmac('sha-256',password.encode('utf-8'), salt, self.iterations_pbkdf_hashing)
        
        secure_module_key_encrypted = AES_GCM.encrypt(self.secure_module_key,password_key)
        with open(backendpath('k.bin'),'wb') as f:
            f.write(secure_module_key_encrypted)
        print('Changed password!')
        
    
    def __init_secure_module(self, password: str) -> None:
        #Init runs, if no existing data.secrets file was found
        #calculates and Hashes the keys and salts needed
        from os import urandom
        salt = urandom(128)
        
        with open(backendpath('s.bin'),'wb') as f:
            f.write(salt)
        
        from hashlib import pbkdf2_hmac
        password_key = pbkdf2_hmac('sha-256',password.encode('utf-8'), salt, self.iterations_pbkdf_hashing)
        
        secure_module_key = AES_GCM.random_key()
        self.secure_module_key = pbkdf2_hmac('sha-256',secure_module_key, urandom(256), 40_000_000)
        secure_module_key_encrypted = AES_GCM.encrypt(self.secure_module_key,password_key)
        with open(backendpath('k.bin'),'wb') as f:
            f.write(secure_module_key_encrypted)
            
        #adds the module secrets
        self.secrets = {}
        self.add_secret('Version','v1.0.0')
        self.add_secret('Key_AES',AES_GCM.random_key())
    
    def AES_Encr(self,data) -> bytes:
        """Encrypts stuff, without having to worry about the key or data type

        Args:
            data (Any): Some object, which will be encrypted. Not bytes!

        Returns:
            bytes: The encrypted data
        """
        data: str = json.dumps(data)
        encr: bytes = AES_GCM.encrypt(data.encode('ascii'),self.aeskey)
        return encr
    
    def AES_Decr(self, data: bytes):
        """Decrypts stuff, without you having to worry about the key or data type

        Args:
            data (bytes): The encrypted bytes from the database

        Returns:
            Any: The decrypted data, in whatever type it was before encryption
        """
        decr: bytes = AES_GCM.decrypt(data,self.aeskey)
        data = json.loads(decr.decode('ascii'))
        return data