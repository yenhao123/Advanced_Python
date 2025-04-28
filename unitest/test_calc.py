import mathlib
import pytest
import sys

#@pytest.mark.skip(reason="Passed it")
@pytest.mark.skipif(sys.version_info < (3, 5), reason="Passed it")
def test_calc_add():
    total = mathlib.calc_total(4, 5)
    assert total == 9

def test_calc_mult():
    total = mathlib.calc_mult(4, 5)
    assert total == 20