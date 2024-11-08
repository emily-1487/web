add_ten = lambda x: x + 10
print(add_ten(5))


def my_fuct(n):
    return lambda x: x * n


double_num = my_fuct(2)
triple_num = my_fuct(3)
print(double_num(5))
print(triple_num(5))
