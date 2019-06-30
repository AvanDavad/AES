from .poly2 import Polynom2, inverse
from .poly_cons import AES_P
from .utils import bitlist_from_hex, hex_from_bitlist
import pickle

def save_s_dict(s_dict, name='s_dict'):
    with open('{}.pkl'.format(name), 'wb') as f:
        pickle.dump(s_dict, f)

def generate_s_dict():
    s_dict = {}
    for i in range(256):
        h_str = hex(i)[2:].zfill(2)
        s_dict[h_str] = s_transform(h_str)
    return s_dict

def get_inverse_dict(s_dict):
    s_inv_dict = {}
    for k, v in s_dict.items():
        s_inv_dict[v] = k
    return s_inv_dict

def s_transform(h_str):
    '''
    This will CALCULATE the s lookup from a byte
    Parameters
    ----------
    h_str: a 2-length string representing a byte
    
    Returns
    ----------
    h_tr_str: a 2-length string representing the the looked-up byte
    
    Examples:
    s_transform('00') -> '63'
    s_transform('af') -> '79'
    '''
    bitlist = bitlist_from_hex(h_str)
    transformed_bitlist = s_bitlist(bitlist)
    return hex_from_bitlist(transformed_bitlist)

def s_bitlist(bitlist):
    exponents = exp_from_bitlist(bitlist)
    p1 = Polynom2(exponents)
    p2 = inverse(p1, AES_P)
    assert len(p2) == 1
    p2 = p2[0]
    b2 = bitlist_from_poly(p2)
    b2 = affine_bitlist_transform(b2)
    b2 = b2[::-1]
    return b2

def exp_from_bitlist(blist):
    exp = []
    for i, val in enumerate(blist):
        if val == 1:
            exp.append(7-i)
    return exp

def bitlist_from_poly(p):
    bitlist = [0 for _ in range(8)]
    for idx in p.exponents:
        bitlist[7-idx] = 1
    return bitlist

def get_affine_col(i):
    col = [0 for _ in range(8)]
    for j in range(5):
        col[(i+j)%8] = 1
    return col

def affine_bitlist_transform(blist):
    tran = [[1,1,0,0,0,1,1,0]]
    for i, val in enumerate(blist):
        if val==1:
            tran.append(get_affine_col(7-i))
    affine = [0 for _ in range(8)]
    for i in range(8):
        affine[i] = sum([c[i] for c in tran]) % 2
    return affine
