"""
    It appears that a parser of some kind is needed for every problem
    in aoc 2024, so I have decided to create a template of sorts that I can
    refer to whenever I attempt the problems
"""

class ParserTemplate:
    def __init__(self, filename = None, test = False):
        if test:
            self.raw_data = ...
        else:
            self.raw_data = self.read_from_file(filename)
        
        self.dataset = self.parse_dataset()
    
    def read_from_file(self, filename):
        raw_data = ""
        with open(filename, "r") as f:
            raw_data = f.read()
        return raw_data
    
    def parse_dataset(self):
        pass

    def __repr__(self):
        # modify this to suit your testing needs
        return f"ParserTemplate({self.dataset!r})"


"""
    Other utilities I found accidentally useful.
"""


# for operations on two 2D lists


def generate_padding(nrows, ncols, pad="*"): return [list(pad*ncols) for _ in range(nrows)]

def padding(raw_data : str):
    n = raw_data.find("\n")

    corner = generate_padding(3, 3)
    hor_slab = generate_padding(3, n)
    ver_slab = generate_padding(n, 3)
    unpadded_list2d =[ list(x) for x in  raw_data.split("\n")]
    pure_padding = hstack(hstack(corner, hor_slab), corner)
    data_padding = hstack(hstack(ver_slab, unpadded_list2d), ver_slab)
    padded_list2d = vstack(vstack(pure_padding, data_padding), pure_padding)
    return padded_list2d


def hstack(x1, x2):
    # check if this is compatible, but i don't care at the moment
    # just check if the rows(x1) == rows(x2)

    # in principle this function can be generalized to an
    # arbitrary number of arguments, but i'm gonna keep it simple
    return [[*a, *b] for (a, b) in zip(x1, x2)]
 

def vstack(x1, x2):
    return x1 + x2