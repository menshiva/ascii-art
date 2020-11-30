import pytest
from roman import Roman

def test_roman_creation():
    assert isinstance(Roman("XX"), Roman)
    
def test_roman_convert_from_int():
    assert Roman.from_int(10).decimal_value == 10

# TODO: implement your own tests here
        
