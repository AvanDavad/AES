from galois import Scalar
from utils import hex_from_bitlist

class Vec4:
    '''
    Representing a column vector.
    this has 4 Scalar instances.
    '''
    def __init__(self, hex_str):
        '''
        e.g.: Vec4('a1 2c 90 01')
        '''
        self.hex_str = hex_str
        assert isinstance(hex_str, str)
        self.b_list = []
        values = hex_str.split()
        assert len(values) == 4
        for val in values:
            self.b_list.append(Scalar(val))
    
    @classmethod
    def from_scalars(cls, scalars):
        assert len(scalars) == 4
        values = []
        for s in scalars:
            values.append(str(s))
        return cls(' '.join(values))
    
    def __add__(self, other):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i] + other.b_list[i])
        return Vec4.from_scalars(b_list)
    
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
        return self.hex_str
    
    def add_scalar(self, s):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i]+s)
        return Vec4.from_scalars(b_list)
    
    def substitute(self, s_dict):
        new_b_list = []
        for b in self.b_list:
            b_hex = hex_from_bitlist(b.bitlist)
            b_hex = s_dict[b_hex]
            new_b_list.append(
                Scalar(b_hex)
            )
        return Vec4.from_scalars(new_b_list)
        
    def rot_word(self, val=1):
        new_b_list = list(self.b_list[val:])
        new_b_list.extend(self.b_list[:val])
        return Vec4.from_scalars(new_b_list)
    
    def mul_scalar(self, s):
        b_list = []
        for i in range(4):
            b_list.append(self.b_list[i]*s)
        return Vec4.from_scalars(b_list)
        
