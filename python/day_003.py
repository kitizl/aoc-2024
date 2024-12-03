import re

class Multiplier:
    def __init__(self, filename = None, test = False):
        if test:
            self.raw_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        else:
            self.raw_data = self.read_from_file(filename)
        
        self.find_multipliers = self.get_multiplier()
        self.find_conditional_multipliers = self.get_conditional_multiplier()
    
    def read_from_file(self, filename):
        raw_data = ""
        with open(filename, "r") as f:
            raw_data = f.read()
        return raw_data.replace("\n","")
    
    def get_multiplier(self):
        # now we need to bracket around for which parts have do() and don't()
        # the "smart" way appears to be using regex to produce a "bracket"
        # of sorts, but i'm not very good with regex

        # the dumb solution appears to be just chomping the string from left
        # to right and just literally flicking a switch on and off

        pattern = r"mul\((\d+),(\d+)\)"
        return re.findall(pattern, self.raw_data)

    def get_conditional_multiplier(self):
        # okay, I found the absolute worst hack ever. The edge case appears
        # to be these dangling do() and don't(). So, I can stick with this
        # if I just alter the data a little bit by adding the invisible do()
        # and don't().
        pattern = r"do\(\)(.*?)don\'t\(\)"
        enabled_string = re.findall(pattern, "do()" + self.raw_data + "don't()")
        multipliers = []
        for match in enabled_string:
            multipliers += re.findall(r"mul\((\d+),(\d+)\)", match)
        return multipliers

    
    def __getitem__(self, pos):
        return self.find_multipliers[pos]

    def __repr__(self):
        # modify this to suit your testing needs
        return f"Multiplier({self.find_multipliers!r})"

def multiply(multiplier):
    acc = 0
    for m in multiplier:
        left, right = (int(n) for n in m)
        acc += left*right
    return acc

def conditional_multiply(multiplier):
    acc = 0
    for m in multiplier.find_conditional_multipliers:
        left, right = (int(n) for n in m)
        acc += left*right
    return acc

def run_all_tests():
    mul = Multiplier(test=True)
    assert str(mul) == f"Multiplier([('2', '4'), ('5', '5'), ('11', '8'), ('8', '5')])"
    assert multiply(mul) == 161
    assert conditional_multiply(mul) == 48


if __name__ == "__main__":
    run_all_tests()

    # if all passes then

    mul = Multiplier(filename="../data/day_003.txt")
    print(multiply(mul))
    print(conditional_multiply(mul))
