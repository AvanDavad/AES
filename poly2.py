class Polynom2:
    '''
    All coefficients are 0 or 1.
    '''
    def __init__(self, exponents):
        self.exponents = sorted(tuple(exponents), reverse=True)
        self.exponents = tuple(self.exponents)
    def _mul(self, coef):
        return Polynom2([c+coef for c in self.exponents])
    def __repr__(self):
        return 'P2{}'.format(self.exponents)
    def copy(self):
        return Polynom2(self.exponents)
    def __add__(self, other):
        new_exponents = []
        exp1 = set(self.exponents)
        exp2 = set(other.exponents)
        exp_add = exp1.symmetric_difference(exp2)
        return Polynom2(exp_add)
    def __mul__(self, other):
        p = Polynom2([])
        for c in other.exponents:
            p = p.copy() + self._mul(c)
        return p
    def __mod__(self, other):
        if len(self.exponents) == 0:
            return self.copy()
        diff = max(self.exponents) - max(other.exponents)
        if diff < 0:
            return self.copy()
        p = other._mul(diff)
        return (self+p) % other
    def __eq__(self, other):
        return self.exponents == other.exponents
    def __hash__(self):
        return (self.exponents).__hash__()

def inverse(p2, mod_p):
    if len(p2.exponents) == 0:
        return [p2.copy()]
    maxexp = max(mod_p.exponents)
    all_poly_list = all_poly(maxexp)
    inv_list = []
    for p in all_poly_list:
        if (p2*p) % mod_p == Polynom2([0]):
            inv_list.append(p)
    return inv_list

def all_poly(maxexp):
    all_poly_list = []
    for maxelem in range(maxexp):
        all_poly_list.extend(Polynom2(exponents) for exponents in all_list(maxelem))
    return all_poly_list

def all_list(maxelem):
    if maxelem == 0:
        return [[0], []]
    all_list_list = []
    for sub_maxelem in range(maxelem):
        all_list_list.extend([[maxelem]+c for c in all_list(sub_maxelem)])
    return all_list_list
