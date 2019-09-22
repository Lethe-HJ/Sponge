# coding:utf-8
#AES-demo

import base64
try:
    from crypto.Cipher import AES
except:
    from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

#加密方法
def encrypt_oracle(text, key):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text.rstrip("\r\n")


#解密方法
def decrypt_oracle(text, key):
    # # 秘钥
    # key = '123456'
    # # 密文
    # text = 'qR/TQk4INsWeXdMSbCDDdA=='
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
    return decrypted_text.rstrip("\r\n")

if __name__ == '__main__':
    print(encrypt_oracle("12345678", "12345678"))
    print(decrypt_oracle("uqSIQXi2cliZ6P2V24J83A==", "PHYZ_PASSWORD_KEY1q2w~!@#$%"))
