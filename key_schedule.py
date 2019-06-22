from vector import Vec4
from matrix import Mat4
import pickle

RCON = []
for c in ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']:
    RCON.append(
        Vec4.from_hexstr('{} 00 00 00'.format(c))
    )

with open('s_dict.pkl', 'rb') as f:
    s_dict = pickle.load(f)


def extend_key(k):
    key_word_list = list(k.c_list)
    for i in range(10):
        for j in range(4):
            col1 = key_word_list[-1]
            col2 = key_word_list[-4]
            if j==0:
                col1 = col1.rot_word()
                col1 = col1.substitute(s_dict)
                col3 = RCON[i]
                new_col = col1 + col2 + col3
            else:
                new_col = col1 + col2
            key_word_list.append(new_col)
    keys = []
    for i in range(11):
        key_chunk = Mat4.from_col_list(list(key_word_list[4*i:4*(i+1)]))
        keys.append(key_chunk)
    return keys