

class OrderingRules:
    def __init__(self, page_ordering_rules):
        # page ordering is a long string that has all the relevant rules
        # 'X1|Y1\nX2|Y2\n...XN|YN'
        # X *has* to come before Y
        self.rules = [tuple(n for n in rule.split("|")) for rule in page_ordering_rules.split("\n")]

    def __getitem__(self, pos):
        return self.rules[pos]
    def __repr__(self):
        output = ""
        for left, right in self.rules:
            output += f"{left}|{right}, "
        
        return f"OrderingRules({output!r})"



class Parser:
    def __init__(self, filename):

        with open(filename, "r") as f:
            self.raw_string = f.read()
        
        self.raw_page_ordering_rules, self.raw_updated_pages = self.raw_string.split("\n\n")

        self.page_ordering_rules = OrderingRules(self.raw_page_ordering_rules)
        self.updated_pages = self.raw_updated_pages.split("\n")
     

def passes_rules(page_row, ordering_rules):
    for rule in ordering_rules:
        match rule:
            case (left, right):
                if page_row.find(left) == -1 or page_row.find(right) == -1:
                    continue
                elif page_row.find(left) > page_row.find(right):
                    return False
    return True

def find_middle_page(page_row):
    pages = page_row.split(",")
    # index of middle page of an odd number of things would be (len(x) - 1)/2
    # if there's something with even number of pages, I'm out

    return int(pages[(len(pages)-1)//2])

def find_answer(pages, rules):
    return sum([find_middle_page(page) for page in pages if passes_rules(page, rules)])

def run_all_tests():
    man = Parser("../tests/day_005.txt")
    # print(man.page_ordering_rules.rules)
    assert passes_rules(man.updated_pages[0], man.page_ordering_rules) == True
    assert passes_rules(man.updated_pages[1], man.page_ordering_rules) == True
    assert passes_rules(man.updated_pages[2], man.page_ordering_rules) == True
    assert passes_rules(man.updated_pages[3], man.page_ordering_rules) == False
    assert passes_rules(man.updated_pages[4], man.page_ordering_rules) == False
    assert passes_rules(man.updated_pages[5], man.page_ordering_rules) == False

    assert find_middle_page("75,29,13") == 29
    assert find_answer(man.updated_pages, man.page_ordering_rules) == 143

if __name__ == "__main__":
    run_all_tests()

    man = Parser("../data/day_005.txt")
    print(find_answer(man.updated_pages, man.page_ordering_rules))
    # sadly, my data structures were not well thought out to do the second part
    # maybe i'll get back to this later

    # i can turn page_row into a list of ints, and then switch to
    # list().index(num) for checking the page order (check membership also first)