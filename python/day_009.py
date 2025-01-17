"""Calculate the final filesystem checksum"""

"""
    Incomplete : Could not figure out what's going wrong.
    
    From a given compressed diskmap, uncompress to get the full filesystem.
    Then, perform the "shuffle" to compact the filesystem such that all
    the data blocks are on the left and all of the free blocks are on the
    right. Afterwards, compute the checksum, which is the ID of the data
    block multiplied by its position.
"""
from collections import Counter

def diskmap_to_blocks(diskmap : str):
    blocks = []
    id = 0
    for parity, char in enumerate(diskmap):
        if parity %2 == 0:
            blocks += [str(id)]*int(char)
            id += 1
        else:
            blocks += ["."]*int(char)
    return blocks

def find_all(test_string : str, char_q : str) -> list[int]:
    """
    Return indices of all occurences of char_q in the 
    given test_string as a list.
    """
    return [i for i, char in enumerate(test_string) if char == char_q]


def compact_blocks(blocks : str) -> str:
    filesystem : str
    free_indices = find_all(blocks, ".")
    filelist = blocks[:]
    moving_blocks = [(index, block) for (index, block) in enumerate(blocks) if block!="."][:len(free_indices)+1:-1]

    for id, (block_id, block) in zip(free_indices, moving_blocks):
        filelist[id] = block
        filelist[block_id] = "."
    # print(filelist)
    return filelist

def calculate_filesystem_checksum(filesystem):
    return sum(i*int(n) for i, n in enumerate(filesystem) if n != ".")

def run_all_tests():
    assert diskmap_to_blocks("12345") == list("0..111....22222")
    assert diskmap_to_blocks("123456") == list("0..111....22222......")
    assert diskmap_to_blocks("1234561") == list("0..111....22222......3")
    assert diskmap_to_blocks("2333133121414131402") == list("00...111...2...333.44.5555.6666.777.888899")
    assert diskmap_to_blocks("233313312141413140211") == list("00...111...2...333.44.5555.6666.777.888899.") + ["10"]
    assert diskmap_to_blocks("90909") == list("0"*9 + "1"*9 + "2"*9)
    assert diskmap_to_blocks("000000000000000000001") == ["10"]
    assert compact_blocks(diskmap_to_blocks("2333133121414131402")) == list("0099811188827773336446555566..............")
    assert calculate_filesystem_checksum(list("0099811188827773336446555566..............")) == 1928
    assert calculate_filesystem_checksum(compact_blocks(diskmap_to_blocks("2333133121414131402"))) == 1928

    print("================")
    print("ALL TESTS PASSED")
    print("================")
    return True
    

if __name__ == "__main__":
    if run_all_tests():
        diskmap = open("data/day_009.txt", "r").read().replace(" ", "")

        # uh oh, this is taking a _long_ time
        # print(Counter(diskmap))
        
        print(
            calculate_filesystem_checksum(
                compact_blocks(
                    diskmap_to_blocks(diskmap)
                )
            )
        )
        