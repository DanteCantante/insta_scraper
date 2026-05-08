from project import check_sys_len
from project import convert_to_digits_photo
from project import convert_to_digits_follow


def test_millions():
    assert convert_to_digits_follow("1M") == 1000000
    assert convert_to_digits_follow("12345M") == 12345000000

def test_point_millions():
    assert convert_to_digits_follow("1.1M") == 1100000

def test_arg_len():
    assert check_sys_len(["abc", "abc"], 2) == True
    assert check_sys_len([1], 3) == False

def test_photo_str():
    assert convert_to_digits_photo("1,432") == 1432
