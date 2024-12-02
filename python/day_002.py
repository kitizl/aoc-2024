from itertools import combinations as select

class Reports:
    def __init__(self, filename = None, test=False):
        if test:
            self.raw_data = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9"
        else:
            self.raw_data = self.read_from_file(filename)
        
        self.reports = self.parse_reports()

    def read_from_file(self, filename):
        raw_data = ""
        with open(filename, "r") as f:
            raw_data = f.read()
        return raw_data
    
    def parse_reports(self):
        return [[int(level) for level in report.split(" ")] for report in self.raw_data.split("\n")]
    def __getitem__(self, position):
        return self.reports[position]  # returns a single report
    def __repr__(self):
        return f"Reports({self.reports!r})"


def is_safe(levels):
    # i can be a smart ass about this
    # update : this was a horrible idea, the Problem Dampener ruined this algorithm
    # now we're simply checking if it's sorted one way or another and then
    # checking to see if everything else works

    is_sorted = all( levels[i] <= levels[i+1] for i in range(len(levels)-1)) or all(levels[i] >= levels[i+1] for i in range(len(levels)-1))

    if not is_sorted:
        return False


    return all( 1 <= abs(levels[i] - levels[i-1]) <= 3 for i in range(1, len(levels))) and \
           all( 1 <= abs(levels[i+1] - levels[i]) <= 3 for i in range(len(levels) - 1))

def is_safe_problem_dampener(levels):
    # i'm gonna use the function that is already kind of built to 
    # basically pop one element out of levels every single time
    # to see if we can "get back to it"
    
    # i know that the generalization of this necessitates me removing
    # n potential unsafe levels, but let's hope n = 1 for this aoc
    # ACTUALLY, AMAZING, WE CAN IMPORT ITERTOOLS FOR THIS
    return is_safe(levels) or any(is_safe(test_level) for test_level in select(levels, len(levels)-1))



def number_of_safe_reports(report_data : Reports, problem_dampener = False):
    return sum(is_safe(report) for report in report_data) if not problem_dampener else sum(is_safe_problem_dampener(report) for report in report_data)


def run_all_tests():
    report_data = Reports(test=True)
    assert str(report_data) == "Reports([[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]])"
    safe_list = [True, False, False, False, False, True]
    for report, safe_check in zip(report_data, safe_list):
        assert is_safe(report) == safe_check
    assert number_of_safe_reports(report_data) == 2
    assert number_of_safe_reports(report_data, True) == 4

if __name__ == "__main__":
    run_all_tests()

    # okay, let's hope everything works now then
    print(number_of_safe_reports(Reports(filename = "../data/day_002.txt")))
    print(number_of_safe_reports(Reports(filename = "../data/day_002.txt"), True))