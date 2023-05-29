from Crypto.Cipher import AES
import base64
class PWEncryptionUtil:
    def __init__(self):
        self.key = bytes("yidaimingjvn2022",encoding='utf8')
    
    # 加密
    def encrypt(self, plaintext) -> None:
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(bytes(plaintext,encoding='utf8'))
        nonce_b64 = str(base64.b64encode(nonce), encoding='utf8')
        ciphertext_b64 = str(base64.b64encode(ciphertext), encoding='utf8')
        tag_b64 = str(base64.b64encode(tag), encoding='utf8')
        
        return ciphertext_b64,nonce_b64,tag_b64
        
    # 解密
    def decrypt(self, ciphertext_b64,nonce_b64,tag_b64) -> str:
        nonce = base64.b64decode(bytes(nonce_b64, encoding='utf8'))
        ciphertext = base64.b64decode(bytes(ciphertext_b64, encoding='utf8'))
        tag = base64.b64decode(bytes(tag_b64, encoding='utf8'))
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)# 验证真实性
            return str(plaintext,encoding="utf8")
        except ValueError:
            return '密钥不正确或消息被破坏'
    
    # 明文验证
    def verifyPlainText(self, now_plaintext,db_plaintext) -> bool:
        if now_plaintext == db_plaintext:
            return True
        else:
            return False
    
    # 密文验证
    def verifyCipherText(self,now_ciphertext,db_ciphertext) -> bool:
        if now_ciphertext == db_ciphertext:
            return True
        else:
            return False
