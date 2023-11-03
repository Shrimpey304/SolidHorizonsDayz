from cryptography.fernet import Fernet
import json
import os
import Utils

class TokenHandler():

    token = ""

    def setToken(self, Token):
        token = Token
        print(token)
        self.tokenEncrypt(token)


    def tokenFetch(self):
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        jsonString = open(log_file_path, 'r').read()
        return(json.loads(jsonString)['token'], json.loads(jsonString)['encrypted'])
        
    def tokenEncrypt(self, token):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_token = fernet.encrypt(token.encode())
        print(encrypted_token, "\n", key)
        Utils.Utils.fetchKeyOnetime(key)
        return encrypted_token, key
        
    def tokenDecrypt(self, key):
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        jsonString = open(log_file_path, 'r').read()
        tokenStringToBytes = bytes(json.loads(jsonString)['token'], 'utf-8')
        fernet = Fernet(key)
        decrypted_token = fernet.decrypt(tokenStringToBytes).decode()
        return decrypted_token
    
    def tokenWrite(self, token, encryption):
        credentialObj = {
                "encrypted" : encryption,
                "token" : token
        }
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        jsonFile = open(log_file_path, 'w')
        jsonFile.write(credentialObj)
    
instance = TokenHandler()
# print(instance.tokenDecrypt(b'zVdAhjqPJEWqLP1BrsKJXKhpMJZ1G7bE8IYo73SqhBw='))