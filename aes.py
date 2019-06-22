import pickle
from galois import COL_MIX, COL_MIX_INV
from key_schedule import extend_key

with open('s_dict.pkl', 'rb') as f:
    s_dict = pickle.load(f)

def encrypt(x, k):
    keys = extend_key(k)
    y = x + keys[0]
    for i in range(1,11):
        y = y.substitute(s_dict)
        y = y.shift_rows()
        if i != 10:
            y = COL_MIX @ y
        y = y + keys[i]
    return y

with open('s_inv_dict.pkl', 'rb') as f:
    s_inv_dict = pickle.load(f)

def decrypt(y, k):
    keys = extend_key(k)
    x = y
    for i in range(10,0,-1):
        x = x + keys[i]
        if i != 10:
            x = COL_MIX_INV @ x
        x = x.shift_rows_inv()
        x = x.substitute(s_inv_dict)
    x = x + keys[0]
    return x