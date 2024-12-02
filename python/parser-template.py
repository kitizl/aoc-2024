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
            raw_data = f.buffer
        return raw_data
    
    def parse_dataset(self):
        pass

    def __repr__(self):
        # modify this to suit your testing needs
        return f"ParserTemplate({self.dataset!r})"