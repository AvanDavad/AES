def bitlist_from_hex(h_str):
    '''
    bitlist_from_hex('a3') -> [1, 0, 1, 0, 0, 0, 1, 1] 
    '''
    int_ = int.from_bytes(bytes.fromhex(h_str), byteorder='little')
    bin_str = bin(int_)[2:].zfill(8)
    return [int(c) for c in list(bin_str)]

def hex_from_bitlist(bitlist):
    '''
    hex_from_bitlist([1, 0, 1, 0, 0, 0, 1, 1]) -> 'a3'
    '''
    int_ = int(''.join([str(c) for c in bitlist]), base=2)
    return hex(int_)[2:].zfill(2)

def exponents_from_bitlist(bitlist):
    '''
    exponents_from_bitlist([1,0,0,1,0,0,1,1]) -> [0, 1, 4, 7]
    '''
    assert len(bitlist) == 8
    exponents = []
    for i in range(8):
        if bitlist[7-i]==1:
            exponents.append(i)
    return exponents

def bitlist_from_exponents(exponents):
    '''
    bitlist_from_exponents([0, 1, 4, 7]) -> [1,0,0,1,0,0,1,1]
    bitlist_from_exponents([]) -> [0,0,0,0,0,0,0,0]
    '''
    if len(exponents) > 0:
        assert min(exponents) >= 0
        assert max(exponents) <= 7
    bitlist = [0 for _ in range(8)]
    for c in exponents:
        bitlist[7-c] = 1
    return bitlist

