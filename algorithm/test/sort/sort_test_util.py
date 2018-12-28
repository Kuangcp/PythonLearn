import random


def generate_data(max_num_value, sort_scale):
    return [random.randint(1, max_num_value) for x in range(sort_scale)]
    # return [1, 2, 3, 45, 6, 7]


def check_sorted(data) -> bool:
    for i in range(0, len(data) - 1):
        if data[i] > data[i + 1]:
            print('error:', data[i], data[i + 1])
            return False
    return True
