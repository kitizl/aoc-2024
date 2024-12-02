


class Parser():
    def __init__(self, filename=None, str=None):

        if filename is None:
            raw_data = self.read_from_string(str)
        else:
            raw_data = self.read_from_filename(filename)

        self.unsorted_data = [[int(a), int(b)] for [a,b] in [row.split() for row in raw_data.split("\n")]]
        self.dataT, self.data = self.parsed_unsorted_data()

    def read_from_string(self, str):
        return str 
    def read_from_filename(self, filename):
        raw_data = ""
        with open(filename, "r") as f:
            raw_data = f.read()
        
        return raw_data


    def parsed_unsorted_data(self):
        unsorted_data_transposed = list(map(list, zip(*self.unsorted_data))) 
        sorted_data_transposed = [sorted(unsorted_data_transposed[0]), sorted(unsorted_data_transposed[1])]
        sorted_data_untransposed = list(map(list, zip(*sorted_data_transposed)))
        return sorted_data_transposed, sorted_data_untransposed
    
    def __repr__(self):
        return f"Parser({self.data!r})"

    def __getitem__(self, position):
        # returns the pair at position i
        return self.data[position]

def total_distance(data : Parser):
    
    distance = sum(abs(left - right) for left, right in data)
    return distance

def similarity_score(data : Parser):
    left, right = data.dataT
    score = 0
    for l in left:
        score += l*(right.count(l))
    return score


def run_tests():
    sample_data = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3"
    parsed_data = Parser(filename = None, str = sample_data)
    assert total_distance(parsed_data) == 11
    assert similarity_score(parsed_data) == 31

if __name__ == "__main__":
    run_tests()

    # assuming it didn't crash, it means the example at least ran smoothly, yay

    actual_parsed_data = Parser(filename = "../data/day_001.txt")

    print(total_distance(actual_parsed_data))
    print(similarity_score(actual_parsed_data))