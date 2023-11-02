from cryptography.fernet import Fernet
import json
import os

class TokenHandler():
    
    def tokenFetch(self):
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'creds.json')
        jsonString = open(log_file_path, 'r').read()
        if(jsonString['encrypted'] == True):
            print("peeper")
        
    def tokenEncrypt(self, token):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(token.encode())
        return encrypted_password, key
        
    def tokenDecrypt(self, key):
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt().decode()
        return decrypted_password
    
instance = TokenHandler()
instance.tokenFetch()