from vector import Column
from utils import hex_from_bitlist

class DataChunk:
    '''
    4 x 4 Matrix.
    this has 4 Column instances.
    '''
    def __init__(self, c_list):
        assert len(c_list) == 4
        self.c_list = c_list
        
    def __repr__(self):
        rows = [[] for _ in range(4)]
        for i, c in enumerate(self.c_list):
            for j in range(4):
                rows[j].append(hex_from_bitlist(c.b_list[j].bitlist))
        for i in range(4):
            rows[i] = ' '.join(rows[i])
        return '\n'.join(rows)
    
    def __add__(self, other):
        c_list = []
        for i in range(4):
            c_list.append(self.c_list[i] + other.c_list[i])
        return DataChunk(c_list)
    
    def substitute(self, s_dict):
        new_c_list = []
        for c in self.c_list:
            new_c_list.append(c.substitute(s_dict))
        return DataChunk(new_c_list)
    
    def shift_rows(self):
        return self._shift_rows(sign=1)
    
    def shift_rows_inv(self):
        return self._shift_rows(sign=-1)
    
    def _shift_rows(self, sign=1):
        dc = self.transposed()
        for i in range(4):
            dc.c_list[i] = dc.c_list[i].rot_word(sign*i)
        dc = dc.transposed()
        return dc
    
    def transposed(self):
        c_list = []
        for row in range(4):
            c_list.append(self.get_row(row))
        return DataChunk(c_list)
    
    def get_row(self, row):
        b_list = []
        for i in range(4):
            b_list.append(self.c_list[i].b_list[row])
        return Column(b_list)
    
    def mul_col(self, col):
        '''
        multiply with a Column
        '''
        b_list = []
        for i in range(4):
            r = self.get_row(i)
            b_list.append(r*col)
        return Column(b_list)
    
    def __matmul__(self, other):
        '''
        matrix multipy
        A @ B
        '''
        c_list = []
        for c in other.c_list:
            c_list.append(self.mul_col(c))
        return DataChunk(c_list)
    
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
                r = r.mul_scalar(s)
            new_rows.append(r)
        new_mat = DataChunk(new_rows)
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
                r = r.add_scalar(s)
            new_rows.append(r)
        new_mat = DataChunk(new_rows)
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
        new_mat = DataChunk(new_rows)
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
                r = self.get_row(rowi).mul_scalar(s) + r
            new_rows.append(r)
        new_mat = DataChunk(new_rows)
        new_mat = new_mat.transposed()
        return new_mat


COL_MIX = DataChunk([Column.from_hexstr('02 01 01 03'), 
                     Column.from_hexstr('03 02 01 01'), 
                     Column.from_hexstr('01 03 02 01'), 
                     Column.from_hexstr('01 01 03 02')])

COL_MIX_INV = DataChunk([Column.from_hexstr('0e 09 0d 0b'), 
                         Column.from_hexstr('0b 0e 09 0d'), 
                         Column.from_hexstr('0d 0b 0e 09'), 
                         Column.from_hexstr('09 0d 0b 0e')])