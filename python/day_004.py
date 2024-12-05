import re
# it's word searching today

# algorithm : look for x's, and then look for an m in the neighborhood
# the moment you find an m, that's the "direction" you want to start 
# searching towards

# better algorithm : to create a kernel/mask of sorts that looks like this
# S**S**S
# *A*A*A*
# **MMM**
# SAMXMAS
# **MMM**
# *A*A*A*
# S**S**S
# but we keep track of specific regions and add the number of occurences
# within those indices (if it is valid, which I'm just going to deal with
# padding the grid with 3 more, as in, an nxn grid gets turned into
# (n+6)x(n+6) so that i don't have to worry about boundary conditions

# EVEN BETTER ALGORITHM : Turns out regex is really good at "just" spotting
# matches in the horizontal. So we simply look for the number of occurences
# of XMAS and SMAX in the regular configuration, 90 degrees rotated, skewed
# upwards, and skewed downwards, in order to catch all possible combinations!

# jesus fucking christ this took _way_ too long to actually capture

# for part two, we only look at the skewed cases and match for MAS and SAM
# but also make sure that both get checked at the same time -- this is a tad bit
# more complicated -- finishing the kernel route would have taken a lot of time
# but it would have been trivial to do this second part

class WordSearch:
    def __init__(self, filename = None, test = False):
        if test:
            self.raw_data = "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX"
        else:
            self.raw_data = self.read_from_file(filename)
        self.dataset = self.listify()
        
    def read_from_file(self, filename):
        raw_data = ""
        with open(filename, "r") as f:
            raw_data = f.read()
        return raw_data
    
    def listify(self):
        return [list(x) for x in self.raw_data.split("\n")]

    def __getitem__(self, index2d):
        x, y = index2d
        return self.dataset[x][y]

    def __len__(self):
        return len(self.dataset)

    def __repr__(self):
        output = ""
        for row in self.dataset:
            output += " ".join(row) + "\n"
        return output


def skew(lst, direction=1):
    result = []
    if direction == 1:
        # skew to the right
        for i, row in enumerate(lst):
            result += [["*"]*(len(lst) - 1 - i) + row + ["*"]*i]
    elif direction == -1:
        # skew to the left
        for i, row in enumerate(lst):
            result += [["*"]*i + row + ["*"]*(len(lst) - 1 - i)]
    else:
        raise NameError
    return result

def rotate(lst):
    # turns out, a "rotation" is the same thing as reversing the
    # rows and performing a transpose, things that are very trivial

    reversed_lst = lst[::-1]
    transposed_reversed_lst = list(map(list, zip(*reversed_lst)))
    return transposed_reversed_lst

def delistify(lst):
    output = ""
    for l in lst:
        output += "".join(l) + "\n"
    return output

# this is for part one
def xmas_occurences(message):
    return len(re.findall("XMAS", message)) + len(re.findall("SAMX", message))

def total_xmas_occurences(ws):
    horizontal = xmas_occurences(delistify(ws.dataset))
    vertical = xmas_occurences(delistify(rotate(ws.dataset)))
    diag_1 = xmas_occurences(delistify(rotate(skew(ws.dataset))))
    diag_2 = xmas_occurences(delistify(rotate(skew(ws.dataset, -1))))

    return horizontal + vertical + diag_1 + diag_2

# this is for part two

def x_mas_occurences(message):
    return len(re.findall("MAS", message)) + len(re.findall("SAM", message))

def total_x_mas_occurences(ws):
    diag_1 = xmas_occurences(delistify(rotate(skew(ws.dataset))))
    diag_2 = xmas_occurences(delistify(rotate(skew(ws.dataset, -1))))

    return diag_1 + diag_2



def run_all_tests():
    ws = WordSearch(test=True)
    assert total_xmas_occurences(ws) == 18
    print(delistify(skew(rotate(skew(ws.dataset, -1)))))
    print(total_x_mas_occurences(ws))
    assert total_x_mas_occurences(ws) == 9

if __name__ == "__main__":
    run_all_tests()

    ws = WordSearch(filename="../data/day_004.txt")
    print(total_xmas_occurences(ws))