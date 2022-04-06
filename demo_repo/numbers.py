class Number:
    def __init__(self, value):
        self.value = value

    def add(self, other):
        return Number(self.value + other.value)

    def __str__(self):
        return f"N({self.value})"

    def __repr__(self):
        return f"N(value={self.value})"


class Integer(Number):
    def __init__(self, value):
        super().__init__(value=int(value))

    def do_some_thing(self):
        number = self.add(Number(2))
        for i in range(number.value):
            number = number.add(Number(i))

        return number
