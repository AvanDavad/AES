from .matrix import Mat4

COL_MIX = Mat4(['02 03 01 01', 
                '01 02 03 01', 
                '01 01 02 03', 
                '03 01 01 02'])

COL_MIX_INV = COL_MIX.inverse()
assert COL_MIX @ COL_MIX_INV == Mat4.eye()