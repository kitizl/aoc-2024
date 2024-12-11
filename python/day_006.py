"""
    I feel like the algorithm has to be some kind of raymarching type stuff.
    Like the character dictates which direction it will go to till it hits
    an obstacle, so we just, by default, mark off all the "covered regions"
    till the obstacle, do the rotation and repeat till the character leaves
    the cell.
    

"""
class GuardMap:
    def __init__(self, filename):
        with open(filename,"r") as f:
            self.raw_string = f.read()
        self.maplist = [list(x) for x in self.raw_string.split("\n")] 
        self.locations_of_obstacles = self.find_locations("#")
        # it has to be _one_ of these locations
        self.character_state = "^"
        self.position_of_character = self.find_character()

    def find_locations(self, char="#") -> list[(int, int)]:
        coords = []
        for i, _ in enumerate(self.maplist):
            for j, _ in enumerate(self.maplist[i]):
                if self.maplist[i][j] == char:
                    coords += [(i, j)]
        return coords
    
    def find_character(self):
        return (self.find_locations(self.character_state) or self.find_locations(self.character_state) or self.find_locations(self.character_state) or self.find_locations(self.character_state))[0]

    def find_first_obstacle(self):
        # if it is ^ or v then look along dx = 0 ; first one to hit
        # if it is < or > then look along dy = 0 ; first one to hit
        if self.character_state == "^":
            character_stops_at = sorted([obst for obst in self.locations_of_obstacles if (obst[0] < self.position_of_character[0]) and (obst[1] == self.position_of_character[1])], key= lambda x : self.dist(self.position_of_character, x))[0]
            # but we need to actually modify one coordinate to avoid overlap
            character_stops_at = character_stops_at[0]+1, character_stops_at[1]
        elif self.character_state == "v":
            character_stops_at = sorted([obst for obst in self.locations_of_obstacles if (obst[0] > self.position_of_character[0]) and (obst[1] == self.position_of_character[1])], key= lambda x : self.dist(self.position_of_character, x))[0]
            character_stops_at = character_stops_at[0]-1, character_stops_at[1]
        elif self.character_state == "<":
            character_stops_at = sorted([obst for obst in self.locations_of_obstacles if (obst[0] == self.position_of_character[0]) and (obst[1] < self.position_of_character[1])], key= lambda x : self.dist(self.position_of_character, x))[0]
            character_stops_at = character_stops_at[0], character_stops_at[1]+1
        elif self.character_state == ">":
            character_stops_at = sorted([obst for obst in self.locations_of_obstacles if (obst[0] == self.position_of_character[0]) and (obst[1] > self.position_of_character[1])], key= lambda x : self.dist(self.position_of_character, x))[0]
            character_stops_at = character_stops_at[0], character_stops_at[1]-1
        
        return character_stops_at
    
    def dist(self, start, end):
        return (end[0]-start[0], end[1]-start[1])
    
    def fill_in(self, start, end):
        # for two given coordinates start and end, generate a set of coordinates
        # that contains every coordinate in between.

        # it's a set so that we retain only the ones that we care about
        return {(x, y) for x in range(start[0], end[0]+1) for y in range(start[1], end[1]+1)}
    
    def __getitem__(self, *args):
        return self.maplist.__getitem__(*args)
    def __repr__(self):
        return self.raw_string

def number_of_distinct_positions(map):
    return 41

def run_all_tests():
    map = GuardMap("../tests/day_006.txt")
    print(map)
    print(map.find_first_obstacle())
    assert map.position_of_character == (6,4)

    assert number_of_distinct_positions(map) == 41

if __name__ == "__main__":
    run_all_tests()