from cryptography.fernet import Fernet

class EncryptDecrypt:


    def generate_key(self):
        key = Fernet.generate_key()
        return key
    
    def encryption(self, sensitive_data):
        fernet_key = self.generate_key()
        fernet_obj = Fernet(fernet_key)
        return fernet_obj.encrypt(sensitive_data.encode()), fernet_key
    
    def decryption(self, fernet_key, encrypted_data):
        key_encoded = Fernet(fernet_key)
        decrypt_msg = key_encoded.decrypt(encrypted_data.encode())
        return str(decrypt_msg, 'UTF-8')
