class Block:

    __slots__ = ('block', 'prev', 'nxt', 'num_elements', 'size')

    def __init__(self, size=10, prev=None, nxt=None):
        self.block = [0] * size # Block size is 10 by default
        self.prev = prev
        self.nxt = nxt
        self.num_elements = 0
        self.size = size

    def __getitem__(self, index):
        if index < 0 or index > 9:
            raise IndexError(f"Cannot index block with index: {index}, must be between 0 and 9")

        return self.block[index]

    def __setitem__(self, index, value):
        if index < 0 or index > self.size - 1:
            raise IndexError(f"Cannot index blcok with index: {index}, must be between 0 and 9")

        self.block[index] = value

    def inc_elements(self):
        self.num_elements = min(self.size, self.num_elements + 1)


    def dec_elements(self):
        self.num_elements = max(0, self.num_elements - 1)

    def is_empty(self):
        return self.num_elements == 0

    def __str__(self):
        return str(self.block)

class Deque:

    __slots__ = ('tail_block', 'head_block', 'num_blocks', 'tail_ptr', 'head_ptr', 'total_elements', 'block_size')

    def __init__(self, block_size=10):
        self.tail_block = Block(block_size)
        self.head_block = self.tail_block
        self.num_blocks = 1
        self.tail_ptr = 0
        self.head_ptr = 0
        self.total_elements = 0
        self.block_size = block_size

    def append(self, value):
        
        self.head_block[self.head_ptr] = value
        self.head_block.inc_elements()
        self.total_elements += 1
        self.head_ptr += 1

        # if head block is full, allocate new block
        if self.head_ptr == self.block_size:
            self.head_block.nxt = Block(self.block_size, self.head_block)
            self.head_block = self.head_block.nxt
            self.head_ptr = 0
            self.num_blocks += 1

    def pop(self):
        
        if self.num_blocks == 1 and self.tail_block.is_empty():
            raise IndexError("Cannot pop from empty list")

        popped_value = self.tail_block[self.tail_ptr]
        self.tail_block[self.tail_ptr] = 0 # Zero out value
        self.total_elements -= 1

        # If at the end of the block, jump to the next one and free old
        if self.tail_ptr == self.block_size - 1:
            self.tail_block = self.tail_block.nxt
            
            del self.tail_block.prev
            self.tail_block.prev = None
            self.tail_ptr = 0
            self.num_blocks -= 1
        else:
            self.tail_ptr += 1
            self.tail_block.dec_elements()

        return popped_value

    def printState(self):

        print(f"tail end state: {self.tail_block}, num_elements: {self.tail_block.num_elements}, tail_ptr: {self.tail_ptr}")

        print(f"head end state: {self.head_block}, num_elements: {self.head_block.num_elements}, head_ptr: {self.head_ptr}")

        if self.num_blocks == 1:
            print("Head and tail block are the same. Only one block.")
        else:
            print(f"Number of blocks: {self.num_blocks}")

        print(f"Total number of elements: {self.total_elements}")

    def __getitem__(self, index):
        
        if index < 0 or index >= self.total_elements:
            raise IndexError(f"Cannot index: {index}")

        # Check if in the first block
        if index < (self.block_size - self.tail_ptr):
            return self.tail_block[self.tail_ptr + index]

        # Chcek if in the last block
        if index >= self.total_elements - self.head_ptr:
            from_last = self.total_elements - index
            return self.head_block[self.head_ptr - from_last]

        # Find which block the element is in
        index_block = ((index - (self.block_size - self.tail_ptr)) // self.block_size) + 1

        if index_block <= self.num_blocks // 2:
            curr_block = self.tail_block.nxt
            curr_index = self.block_size - self.tail_ptr
            while (index - curr_index) >= self.block_size:
                curr_block = curr_block.nxt
                curr_index += self.block_size

            return curr_block[index - curr_index]
        
        else:
            curr_block = self.head_block.prev
            curr_index = self.total_elements - self.head_ptr - 1
            while (curr_index - index) >= self.block_size:
                curr_block = curr_block.prev
                curr_index -= self.block_size

            return curr_block[self.block_size - (curr_index - index + 1)]


def printLn():
    print("\n" + "-" * 30 + "\n")

def quickTest():

    d = Deque()
    ref = []

    for i in range(60):
        d.append(i)
        ref.append(i)

    for _ in range(7):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_13a: pop mismatch, deque={actual}, ref={expected}"
        )

    d.printState()
    printLn()

    for i in range(len(ref) // 2, len(ref)):
        actual = d[i]
        expected = ref[i]
        print(actual, i)
        assert actual == expected, (
            f"test_13b: mismatch at index {i}, deque={actual}, ref={expected}"
        )

def main():

    quickTest()


if __name__ == "__main__":
    main()
