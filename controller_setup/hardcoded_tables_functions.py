"""Add here the functions you wish to use as callbacks for the tables.

After a read, modbus_tk returns a tuple. The interpretation of the tuple is defined here
and is dependent on the register type. This is especially important for signed values.
"""

def bits16_to_bits32(int_tuple):
    return int(0x10000*int_tuple[0]+int_tuple[1])
def lambdax_x0(x):
    return x[0]
def concatenate(_strings):
    "".join(_strings)
def bits16_to_bits32_swap(int_tuple):
    return int(0x10000*int_tuple[1]+int_tuple[0])

from struct import pack, unpack
def unsigned_bits16_to_swap_float(_tuple):
    swapped_bytes = pack(">HH", _tuple[1], _tuple[0])
    float_result = unpack(">f", swapped_bytes)
    return float_result[0]
def signed_bits16_to_swap_float(_tuple):
    swapped_bytes = pack(">hh", _tuple[1], _tuple[0])
    float_result = unpack(">f", swapped_bytes)
    return float_result[0]
# join is way faster than reduce(operator.add, _strings)
# https://stackoverflow.com/questions/3525359/python-sum-why-not-strings

"""Register your new function here, but do not change the already associated 0 <-> 16bits answer,
1 <-> two 16bits to 32"""
callback_choices = (
    (1, "two 16bits to form a 32bits, for data_format=>HH"),
    (0, "length one answer, ex (xxx,)"),
    (2, "concatenate strings"),
    (3, "swapped version of 2*16bits->1*32bits, make sure your data_format is correct, so either unsigned >HH or signed >hh"),
    (4, "unsigned 16bits to swap float"),
    (5, "signed 16bits to swap float"),
)
callback_map = {
    0:lambdax_x0,
    1:bits16_to_bits32,
    2:concatenate,
    3:bits16_to_bits32_swap,
    4:unsigned_bits16_to_swap_float,
    5:signed_bits16_to_swap_float
}