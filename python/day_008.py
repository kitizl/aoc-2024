from collections import defaultdict
import itertools

def vec_manhattan_dist(a : list[int], b : list[int]) -> int:
    assert len(a) == len(b)
    return [a[0]-b[0], a[1]-b[1]]

"""
An Antinode occurs at any point that is perfectly in line with two antennas
of the same frequency - but only when one of the antennas is twice as far
away as the other. This means that for any pair of antennas with the same
frequency, there are two antinodes, one on either side of them.
"""

class Antenna:
    """
    An Antenna is an object located at a point (x, y) that emits a frequency
    represented by a lower case letter, an upper case letter, or a single 
    digit. 
    """
    def __init__(self, x, y, freq):
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]
        self.freq = freq
    
    def __repr__(self):
        return f"Antenna({self.x!r}, {self.y!r}, {self.freq!r})"
    

class Map:
    """
    A Map is a 2D grid where distances are measured with the taxicab metric.
    The map is marked with locations of the antennas emitting a specific
    frequency.
    """
    def __init__(self, filename):
        with open(filename) as f:
            self.raw_string = f.read()
        
        self.raw_map = self.string_to_list(self.raw_string)
        self.height = len(self.raw_map) # number of rows
        self.width = len(self.raw_map[0]) # number of columns

    
    def __contains__(self, pos):
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width

    
    def __getitem__(self, *args):
        return self.raw_map.__getitem__(*args)

    def string_to_list(self, string : str, sep : str="") -> list[list[str]]:
        rows = string.split("\n")
        if sep == "":
            return [list(row) for row in rows]
        else:
            return [elem for row in rows for elem in row.split(sep)]
            


def antenna_locations(map : Map) -> list[Antenna]:
    antennas = []
    for i, row in enumerate(map.raw_map):
        for j, val in enumerate(row):
            if val.isalpha() or val.isdigit():
                antennas += [Antenna(i, j, val)]
    return antennas

def add(v1, v2):
    # vector addition
    return [i+j for i, j in zip(v1, v2)]

def antinode_locations(map : Map, debug=False) -> set[tuple[int, int]]:
    anti_pos = []
    antennas = antenna_locations(map)
    ant_groupedby_frequency = defaultdict(list)
    for ant in antennas:
        ant_groupedby_frequency[ant.freq].append(ant)
    
    for frequency, ants in ant_groupedby_frequency.items():
        # look at the ants pairwise
        for ant1, ant2 in itertools.combinations(ants, 2):
            # vector pointing *from* ant2 *to* ant1
            gap = vec_manhattan_dist(ant1.pos, ant2.pos)
            # coordinates of new potential antinodes
            option_1 = add(ant1.pos, gap)
            option_2 = add(ant2.pos, [-g for g in gap]) # inverting is hard
            if option_1 in map:
                anti_pos.append(tuple(option_1))
            if option_2 in map:
                anti_pos.append(tuple(option_2))
    if debug:
        debugmap = map.raw_map
        for (i, j) in anti_pos:
            debugmap[i][j] = "#" if debugmap[i][j] == "." else "+"
        print("\n".join("".join(row) for row in debugmap))
    return set(anti_pos)


def calculate_antinode_locations(map : Map, debug=False) -> int:
    """
    For a given map with Antennas emitting a specific frequency, return
    the total number of unique locations within the bounds of the given
    map that contain an antinode. 
    """
    return len(antinode_locations(map, debug))

def run_all_tests():
    assert (Antenna(0, 0, "a").freq == Antenna(1, 1, "a").freq) == True
    assert (Antenna(0, 0, "a").freq == Antenna(1, 1, "A").freq) == False
    assert str(antenna_locations(Map("../tests/day_008.txt"))[0])  == str(Antenna(1, 8, '0'))
    assert calculate_antinode_locations(map=Map("../tests/day_008.txt")) == 14

    return True


run_all_tests()

print(calculate_antinode_locations(map=Map("../data/day_008.txt")))


# i thought this might be a catch lol, but okay.
# part two requires you to find every single possible antinode in the grid
# not just the two closest ones ; this will require a bit of generalizing 
# in the antinode_locations() function
# we start from the first antenna, and basically march in 1*gap, 2*gap, and 
# so on till we leave the map, then we do -2*gap, -3*gap and so on till we
# leave the map