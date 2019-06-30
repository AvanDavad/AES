import pickle
import os
here = os.path.abspath(os.path.dirname(__file__))

from .s_box import generate_s_dict, save_s_dict, get_inverse_dict

filename = os.path.join(here, 's_dict.pkl')
if not os.path.isfile(filename):
    s_dict = generate_s_dict()
    save_s_dict(s_dict, filename)
else:
    with open(filename, 'rb') as f:
        s_dict = pickle.load(f)

filename = os.path.join(here, 's_inv_dict.pkl')
if not os.path.isfile(filename):
    s_inv_dict = get_inverse_dict(s_dict)
    save_s_dict(s_inv_dict, filename)
else:
    with open(filename, 'rb') as f:
        s_inv_dict = pickle.load(f)
