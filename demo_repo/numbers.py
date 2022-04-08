class Number:
    def __init__(self, value):
        self.value = value

    def add(self, other):
        return Number(self.value + other.value)

    def __str__(self):
        return f"N({self.value})"

    def __repr__(self):
        return f"N(value={self.value})"


class Float(Number):
    def integer(self):
        return Integer(self.value)

    def fractional(self):
        return Float(self.value - int(self.value))

    def invert(self):
        self.value = 1 / self.value

    def _check_positive(self):
        assert self.value > 0


class Integer(Number):
    def __init__(self, value):
        super().__init__(value=int(value))

    def do_some_thing(self):
        number = self.add(Number(2))
        for i in range(number.value):
            number = number.add(Number(i))

        return number


def test_float():
    x = 3.14
    f = Float(x)
    f._check_positive()
    assert f.integer().value == int(x)
    assert f.fractional().value == (x - int(x))
