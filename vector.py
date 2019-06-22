from galois import Scalar
from utils import hex_from_bitlist

class Vec4:
    '''
    Representing a vector.
    this has 4 Scalar instances.
    '''
    def __init__(self, hex_str):
        '''
        e.g.: Vec4('a1 2c 90 01')
        '''
        self.hex_str = hex_str
        assert isinstance(hex_str, str)
        self.values = []
        values = hex_str.split()
        assert len(values) == 4
        for val in values:
            self.values.append(Scalar(val))
    
    @classmethod
    def from_scalars(cls, scalars):
        assert len(scalars) == 4
        values = []
        for s in scalars:
            assert isinstance(s, Scalar)
            values.append(str(s))
        return cls(' '.join(values))
    
    def __add__(self, other):
        '''
        Add a Vec4 or a Scalar
        e.g.:
          v0 = Vec4('c9 12 31 6a')
          v1 = Vec4('32 cc d0 0b')
          v0 + v1 ->
          v0 + Scalar('ff') ->
          v0 + 'ff' ->
        '''
        be_added = []
        if isinstance(other, Vec4):
            be_added = other.values
        elif isinstance(other, Scalar):
            be_added = [other for _ in range(4)]
        elif isinstance(other, str):
            be_added = [Scalar(other) for _ in range(4)]
        else:
            raise ValueError('cannot add {} to Vec4'.format(type(other)))
        scalars = []
        for i in range(4):
            scalars.append(self.values[i] + be_added[i])
        return Vec4.from_scalars(scalars)
    
    def __mul__(self, other):
        '''
        inner product
        '''
        pr = []
        for i in range(4):
            pr.append(self.values[i]*other.values[i])
        sum_ = pr[0] + pr[1] + pr[2] + pr[3]
        return sum_
    
    def __repr__(self):
        return self.hex_str
    
    def add_scalar(self, s):
        values = []
        for i in range(4):
            values.append(self.values[i]+s)
        return Vec4.from_scalars(values)
    
    def substitute(self, s_dict):
        new_values = []
        for b in self.values:
            b_hex = hex_from_bitlist(b.bitlist)
            b_hex = s_dict[b_hex]
            new_values.append(
                Scalar(b_hex)
            )
        return Vec4.from_scalars(new_values)
        
    def rot_word(self, val=1):
        new_values = list(self.values[val:])
        new_values.extend(self.values[:val])
        return Vec4.from_scalars(new_values)
    
    def mul_scalar(self, s):
        values = []
        for i in range(4):
            values.append(self.values[i]*s)
        return Vec4.from_scalars(values)
        
