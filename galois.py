from poly2 import Polynom2, inverse, AES_P
from utils import (bitlist_from_hex, 
                   hex_from_bitlist, 
                   exponents_from_bitlist, 
                   bitlist_from_exponents)



class Scalar:
    '''
    element of Galois Field (256)
    this is actually a byte
    '''
    def __init__(self, h_str):
        self.bitlist = bitlist_from_hex(h_str)
        exponents = exponents_from_bitlist(self.bitlist)
        self._poly = Polynom2(exponents)
        
    def __add__(self, other):
        new_poly = self._poly + other._poly
        return Scalar.from_polynom2(new_poly)
    
    def __mul__(self, other):
        new_poly = (self._poly * other._poly) % AES_P
        return Scalar.from_polynom2(new_poly)
    
    def __repr__(self):
        return hex_from_bitlist(self.bitlist)
    
    def inverse(self):
        p_inv = inverse(self._poly, AES_P)[0]
        return Scalar.from_polynom2(p_inv)
    
    @classmethod
    def from_bitlist(cls, bitlist):
        h_str = hex_from_bitlist(bitlist)
        return cls(h_str)
    
    @classmethod
    def from_polynom2(cls, poly):
        exponents = poly.exponents
        bitlist = bitlist_from_exponents(exponents)
        return cls.from_bitlist(bitlist)
    

