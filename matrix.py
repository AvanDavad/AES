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
    
    @classmethod
    def eye(cls):
        c_list = []
        for i in range(4):
            c_list.append(Vec4.eye(i))
        return cls.from_col_list(c_list)
    
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
    
    def inverse(self):
        r_tran = RowTransform()
        mat = self
        inv_mat = Mat4.eye()
        for i in range(4):
            mat = r_tran.fit_transform(mat, i)
            inv_mat = r_tran.transform(inv_mat)
        return inv_mat
    

class RowTransform:
    '''
    convinient class for matrix inversion
    '''
    def fit(self, mat, idx):
        self.idx = idx
        self.col = mat.get_col(idx)
        self.s_inv = mat.get_scalar(idx,idx).inverse()
    
    def transform(self, mat):
        r_list = [None for _ in range(4)]
        row = mat.get_row(self.idx)
        row = row*self.s_inv
        r_list[self.idx] = row
        for i in range(4):
            if i == self.idx:
                continue
            s_idx = self.col.values[i]
            normed_row = mat.get_row(self.idx) * self.s_inv
            r_list[i] = (mat.get_row(i) + 
                         normed_row * s_idx)
        return Mat4.from_row_list(r_list)
    
    def fit_transform(self, mat, idx):
        self.fit(mat, idx)
        return self.transform(mat)
    