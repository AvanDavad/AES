from galois import Scalar
from utils import hex_from_bitlist

class Vec4:
    '''
    Representing a column vector.
    this has 4 Scalar instances.
    '''
    def __init__(self, b_list):
        assert len(b_list) == 4
        self.b_list = b_list
        
    def __add__(self, other):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i] + other.b_list[i])
        return Vec4(b_list)
    
    def __mul__(self, other):
        '''
        scalar product
        '''
        pr = []
        for i in range(4):
            pr.append(self.b_list[i]*other.b_list[i])
        sum_ = pr[0] + pr[1] + pr[2] + pr[3]
        return sum_
    
    def __repr__(self):
        hex_list = []
        for i in range(4):
            hex_list.append(
                hex_from_bitlist(self.b_list[i].bitlist)
            )
        return '\n'.join(hex_list)
    
    def add_scalar(self, s):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i]+s)
        return Vec4(b_list)
    
    @classmethod
    def from_hexstr(cls, hex_str):
        '''
        e.g.:
        Vec4.from_hexstr('a1 2c 90 01')
        '''
        hex_str_list = hex_str.split()
        b_list = []
        for hstr in hex_str_list:
            b_list.append(
                Scalar(hstr)
            )
        return cls(b_list)
    
    @classmethod
    def from_scalars(cls, scalars):
        return cls(scalars)
    
    def substitute(self, s_dict):
        new_b_list = []
        for b in self.b_list:
            b_hex = hex_from_bitlist(b.bitlist)
            b_hex = s_dict[b_hex]
            new_b_list.append(
                Scalar(b_hex)
            )
        return Vec4(new_b_list)
        
    def rot_word(self, val=1):
        new_b_list = list(self.b_list[val:])
        new_b_list.extend(self.b_list[:val])
        return Vec4(new_b_list)
    
    def mul_scalar(self, s):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i]*s)
        return Vec4(b_list)
        
