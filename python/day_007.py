import itertools

"""
    Note : improvements can be made by generalizing some of the functions.
    But I will leave that as an exercise to future me.
"""


class Equation:
    """
    An Equation is an object where a test value is paired with a list of numbers. 
    """

    def __init__(self, raw_string):
        self.test_val, self.operands = self.parse_string(raw_string)
    def parse_string(self, raw_string):
        test_val, raw_operands = raw_string.split(":")
        operands = raw_operands.strip().split(" ")
        return int(test_val), [int(v) for v in operands]
    def __repr__(self):
        return f"Equation({self.test_val!r}, {self.operands!r})"

def parse_input(filename : str) -> list[Equation]:
    with open(filename,"r") as f:
        raw_data = f.read()
    return [Equation(raw_string) for raw_string in raw_data.split("\n")]


def add(op1, op2):
    return op1 + op2

def multiply(op1, op2):
    return op1 * op2

def concat(op1, op2):
    return int(str(op1)+str(op2))


def evaluate_expression(operands, operations):
    """
    A function that returns true if the operands, operated by 
    either add (+) or multiply (*) would give the value. These operations
    are always from left to right, and not by precedence.

    Left-to-right precedence operations can be written as follows : for
    operands given by m1, m2, m3, ... and binary operation given by @, in 
    infix notation, you can write
    (((m1 @ m2) @ m3) @ m4) ...

    But we can use the fact that this can still commute overall, and rewrite to
    (m4 @ (m 3 @ (m2 @ m1)))

    If I was writing in a language better built for recursion I'd do that, but
    I have a more braindead idea than that.
    """
    acc = 0
    operators = [add] + list(operations) # the first step is initializing the acc

    for val, op in zip(operands, operators):
        acc = op(acc, val)
    return acc


def passes_test(eq : Equation) -> bool:
    """
    A function that returns true if, for some combination of operations, the
    operands of the passed Equation eq evaluate (through evaluate_expression())
    to the test value.
    """
    # number of "slots" the operators can sit in is len(dummy) - 1

    number_of_slots = len(eq.operands) - 1

    operations = [add, multiply]

    for op_order in itertools.product(operations, repeat=number_of_slots):
        if evaluate_expression(eq.operands, op_order) == eq.test_val:
            return True
    return False

def passes_test_with_concat(eq:Equation) -> bool:
    number_of_slots = len(eq.operands) - 1

    operations = [add, multiply, concat]

    for op_order in itertools.product(operations, repeat=number_of_slots):
        if evaluate_expression(eq.operands, op_order) == eq.test_val:
            return True
    return False



def total_calibration_result(equations : list[Equation]):
    """
    Given a list of equations with a test value and a list of operands,
    add the test values of equations that pass the test.
    """

    return sum([eq.test_val for eq in equations if passes_test(eq)])

def total_calibration_result_with_concat(equations : list[Equation]):

    return sum([eq.test_val for eq in equations if passes_test_with_concat(eq)])

def run_tests():

    assert str(Equation("190: 10 19")) == "Equation(190, [10, 19])"
    # my own testing if my evaluator works
    assert evaluate_expression([1,1,1,1],[add,add,add]) == 4
    assert evaluate_expression([1,0,1,1], [multiply, multiply, multiply, multiply]) == 0
    # let's test one of the test cases
    assert evaluate_expression([81, 40, 27], [add, multiply]) == 3267
    assert evaluate_expression([81, 40, 27], [multiply, add]) == 3267
    # now let's evaluate the test cases
    assert [passes_test(eq) for eq in parse_input("../tests/day_007.txt")] == [True, True, False, False, False, False, False, False, True]
    assert total_calibration_result(parse_input("../tests/day_007.txt")) == 3749

    # part two includes concat!

    assert total_calibration_result_with_concat(parse_input("../tests/day_007.txt")) == 11387
    return True

run_tests()

# part one
print(total_calibration_result(parse_input("../data/day_007.txt")))

# part two // Note : seems to take a way while longer
print(total_calibration_result_with_concat(parse_input("../data/day_007.txt")))