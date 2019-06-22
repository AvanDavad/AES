from galois import Scalar
from vector import Vec4
from utils import hex_from_bitlist

class Mat4:
    '''
    4 x 4 Matrix.
    Immutable, should not change anything inplace.
    Its elements are from GaloisField(256)
    '''
    def __init__(self, rows):
        self.rows = rows
        assert len(rows) == 4
        self.r_list = []
        for row in rows:
            assert isinstance(row, str)
            self.r_list.append(Vec4(row))
        self.c_list = []
        for col_idx in range(4):
            scalars = []
            for row_idx in range(4):
                scalars.append(self.r_list[row_idx].values[col_idx])
            column = Vec4.from_scalars(scalars)
            self.c_list.append(column)
    
    @classmethod
    def from_col_list(cls, c_list):
        assert len(c_list) == 4
        rows = []
        for row_idx in range(4):
            scalars = []
            for col_idx in range(4):
                assert isinstance(c_list[col_idx], Vec4)
                scalars.append(str(c_list[col_idx].values[row_idx]))
            rows.append(' '.join(scalars))
        return cls(rows)
    
    @classmethod
    def from_row_list(cls, r_list):
        assert len(r_list) == 4
        rows = []
        for row_idx in range(4):
            assert isinstance(r_list[row_idx], Vec4)
            scalars = []
            for col_idx in range(4):
                scalars.append(str(r_list[row_idx].values[col_idx]))
            rows.append(' '.join(scalars))
        return cls(rows)
    
    @classmethod
    def rand(cls):
        r_list = [Vec4.rand() for _ in range(4)]
        return Mat4.from_row_list(r_list)
    
    def __repr__(self):
        return '\n'.join(self.rows)
    
    def __add__(self, other):
        be_added = []
        if isinstance(other, Mat4):
            be_added = other.c_list
        elif isinstance(other, Scalar):
            be_added = [other for _ in range(4)]
        elif isinstance(other, str):
            be_added = [Scalar(other) for _ in range(4)]
        else:
            raise ValueError('cannot add {} to Mat4'.format(type(other)))
        c_list = []
        for i in range(4):
            c_list.append(self.c_list[i] + be_added[i])
        return Mat4.from_col_list(c_list)
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def substitute(self, s_dict):
        new_c_list = []
        for c in self.c_list:
            new_c_list.append(c.substitute(s_dict))
        return Mat4.from_col_list(new_c_list)
    
    def shift_rows(self):
        return self._shift_rows(sign=1)
    
    def shift_rows_inv(self):
        return self._shift_rows(sign=-1)
    
    def _shift_rows(self, sign=1):
        r_list = []
        for i in range(4):
            r_list.append(self.r_list[i].rot_word(sign*i))
        return Mat4.from_row_list(r_list)
    
    def transposed(self):
        return Mat4.from_col_list(self.r_list)
    
    def get_row(self, idx):
        return self.r_list[idx]
    
    def get_col(self, idx):
        return self.c_list[idx]
    
    def get_scalar(self, i, j):
        return self.r_list[i].values[j]
    
    def mul_col(self, col):
        '''
        multiply with a Vec4 column vector
        '''
        scalars = []
        for i in range(4):
            scalars.append(
                self.r_list[i].dot(col)
            )
        return Vec4.from_scalars(scalars)
    
    def __matmul__(self, other):
        '''
        matrix multipy
        A @ B
        '''
        c_list = []
        for c in other.c_list:
            c_list.append(self.mul_col(c))
        return Mat4.from_col_list(c_list)
    
    def mul_row(self, row_idx, s):
        '''
        multiply a row by s
        row_idx: row index (0..3)
        s: Scalar
        '''
        new_rows = []
        for i in range(4):
            r = self.get_row(i)
            if i == row_idx:
                r = r*s
            new_rows.append(r)
        new_mat = Mat4.from_col_list(new_rows)
        new_mat = new_mat.transposed()
        return new_mat
    
    def add_row(self, row_idx, s):
        '''
        add a scalar to a row
        '''
        new_rows = []
        for i in range(4):
            r = self.get_row(i)
            if i == row_idx:
                r = r+s
            new_rows.append(r)
        new_mat = Mat4.from_col_list(new_rows)
        new_mat = new_mat.transposed()
        return new_mat
    
    def add_rowi_to_rowj(self, rowi, rowj):
        '''
        add row `rowi` to row `rowj`
        '''
        new_rows = []
        for i in range(4):
            r = self.get_row(i)
            if i == rowj:
                r = r + self.get_row(rowi)
            new_rows.append(r)
        new_mat = Mat4.from_col_list(new_rows)
        new_mat = new_mat.transposed()
        return new_mat
    
    def mul_add_row(self, rowi, s, rowj):
        '''
        multiply row with index `rowi` by s and add to row
        with index `rowj`
        '''
        new_rows = []
        for i in range(4):
            r = self.get_row(i)
            if i == rowj:
                r = self.get_row(rowi)*s + r
            new_rows.append(r)
        new_mat = Mat4.from_col_list(new_rows)
        new_mat = new_mat.transposed()
        return new_mat

COL_MIX = Mat4(['02 03 01 01', 
                '01 02 03 01', 
                '01 01 02 03', 
                '03 01 01 02'])

COL_MIX_INV = Mat4(['0e 0b 0d 09', 
                    '09 0e 0b 0d', 
                    '0d 09 0e 0b', 
                    '0b 0d 09 0e'])