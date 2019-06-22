from galois import Scalar

class Vec4:
    '''
    Representing a vector.
    Immutable, should not change anything inplace.
    this has 4 Scalar instances.
    Its elements are from GaloisField(256)
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
    
    @classmethod
    def rand(cls):
        scalars = [Scalar.rand() for _ in range(4)]
        return Vec4.from_scalars(scalars)
    
    def __add__(self, other):
        '''
        Add a Vec4 or a Scalar
        e.g.:
          v0 = Vec4('78 ae d9 ab')
          v1 = Vec4('27 38 3c 10')
          v0 + v1 -> 5f 96 e5 bb
          v0 + Scalar('ff') -> 87 51 26 54
          v0 + 'ff' -> 87 51 26 54
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
        Multiply by a Vec4 or a Scalar
        e.g.:
          v0 = Vec4('78 ae d9 ab')
          v1 = Vec4('27 38 3c 10')
          v0 * v1 -> ea 15 9a 5e
          v0 * Scalar('ff') -> bd 3a f5 14
          v0 * 'ff' -> bd 3a f5 14
        '''
        be_multiplied = []
        if isinstance(other, Vec4):
            be_multiplied = other.values
        elif isinstance(other, Scalar):
            be_multiplied = [other for _ in range(4)]
        elif isinstance(other, str):
            be_multiplied = [Scalar(other) for _ in range(4)]
        else:
            raise ValueError('cannot multiply {} with Vec4'.format(type(other)))
        scalars = []
        for i in range(4):
            scalars.append(self.values[i]*be_multiplied[i])
        return Vec4.from_scalars(scalars)
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __repr__(self):
        return self.hex_str
    
    def dot(self, other):
        '''
        inner product
        '''
        pr = []
        for i in range(4):
            pr.append(self.values[i]*other.values[i])
        sum_ = pr[0] + pr[1] + pr[2] + pr[3]
        return sum_
    
    def substitute(self, s_dict):
        scalars = []
        for val in self.values:
            looked_up_val = s_dict[str(val)]
            scalars.append(
                Scalar(looked_up_val)
            )
        return Vec4.from_scalars(scalars)
        
    def rot_word(self, val=1):
        scalars = list(self.values[val:])
        scalars.extend(self.values[:val])
        return Vec4.from_scalars(scalars)
        
