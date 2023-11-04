from cryptography.fernet import Fernet
import json
import os
import Utils

class TokenHandler():

    token = ""

    def tokenFetch(self):
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        jsonString = open(log_file_path, 'r').read()
        return(json.loads(jsonString)['token'], json.loads(jsonString)['encrypted'])
        
    #create a key and encrypts the token with the key, it will save both the key and the token into utils
    def tokenEncrypt(self, token):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_token = fernet.encrypt(token.encode())
        TokenHandler.tokenWrite(self, encrypted_token, True)
        Utils.Utils.fetchKey(key.decode())
        Utils.Utils.fetchDecryptedToken(token)
        return key
        
    def tokenDecrypt(self, key):
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        jsonString = open(log_file_path, 'r').read()
        tokenStringToBytes = bytes(json.loads(jsonString)['token'], 'utf-8')
        fernet = Fernet(key)
        decrypted_token = fernet.decrypt(tokenStringToBytes).decode()
        Utils.Utils.fetchDecryptedToken(decrypted_token)
        return True
    
    def tokenWrite(self, token, encryption):
        credentialObj = {
                "encrypted" : encryption,
                "token" : token.decode()
        }
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'Content', 'Credentials', 'Credentials.json')
        with open(log_file_path, 'w') as f:
            json.dump(credentialObj, f)
        
        
instance = TokenHandler()
# key = instance.tokenEncrypt('randomtokenidk')
# print(key)
# print(instance.tokenDecrypt(key))
# print(Utils.K)
# print(instance.tokenDecrypt(b'zVdAhjqPJEWqLP1BrsKJXKhpMJZ1G7bE8IYo73SqhBw='))