from poly2 import Polynom2, inverse
from poly_cons import AES_P
from utils import (bitlist_from_hex, 
                   hex_from_bitlist, 
                   exponents_from_bitlist, 
                   bitlist_from_exponents)
import random


class Scalar:
    '''
    element of GaloisField(256)
    this is actually a byte
    '''
    def __init__(self, h_str):
        '''
        e.g.: Scalar('a8')
        '''
        self.h_str = h_str
        assert len(h_str) == 2
        for c in h_str:
            assert c in '0123456789abcdef'
        self.bitlist = bitlist_from_hex(h_str)
        exponents = exponents_from_bitlist(self.bitlist)
        self._poly = Polynom2(exponents)
    
    @classmethod
    def from_bitlist(cls, bitlist):
        h_str = hex_from_bitlist(bitlist)
        return cls(h_str)
    
    @classmethod
    def from_polynom2(cls, poly):
        exponents = poly.exponents
        bitlist = bitlist_from_exponents(exponents)
        return cls.from_bitlist(bitlist)
    
    @classmethod
    def rand(cls):
        bitlist = []
        for i in range(8):
            bitlist.append(random.randint(0,1))
        return cls.from_bitlist(bitlist)
    
    def __add__(self, other):
        assert isinstance(other, Scalar)
        new_poly = self._poly + other._poly
        return Scalar.from_polynom2(new_poly)
    
    def __mul__(self, other):
        assert isinstance(other, Scalar)
        new_poly = (self._poly * other._poly) % AES_P
        return Scalar.from_polynom2(new_poly)
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __repr__(self):
        return self.h_str
    
    def inverse(self):
        p_inv = inverse(self._poly, AES_P)[0]
        return Scalar.from_polynom2(p_inv)
    

