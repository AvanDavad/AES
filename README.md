API for using Advanced Encryption Standard.

'''python
from aes_api import encrypt, decrypt, Mat4
x = Mat4.rand() # my secret message
key = Mat4.rand()
y = encrypt(x, key)

assert x == decrypt(y, key)
'''
