import sys
sys.path.append("..")
import three
import first.one as one


def two_a():
    print('seconde.two', 'a')
    one.one_a()


if __name__ == "__main__":
    two_a()
    three.three_a()
    one.one_a()
