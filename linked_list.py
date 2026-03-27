class Node:

    __slots__ = ('val', 'nxt')

    def __init__(self, val, nxt=None):
        self.val = val
        self.nxt = nxt

class LLQueue:

    __slots__ = ('head', 'tail')

    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, val):

        if not self.head:
            self.head = Node(val)
            self.tail = self.head
        else:
            self.tail.nxt = Node(val)
            self.tail = self.tail.nxt

    def pop(self):

        if not self.head:
            raise IndexError("Cannot pop from empty list")

        curr = self.head

        res = curr.val

        self.head = self.head.nxt
        
        if not self.head:
            self.tail = None

        # Technically unnecessary because of reference count, but used for idea
        del curr

        return res

    def peek(self):

        if not self.head:
            raise IndexError("Cannot peek from empty list")

        return self.head.val

    def isEmpty(self):

        return self.head is None

def quickTest():

    queue = LLQueue()

    for i in range(5):
        queue.append(i)

    for _ in range(5):
        print(queue.pop())

    try:
        queue.pop()
    except IndexError as e:
        print(e)

def main():
   
    quickTest()

if __name__ == "__main__":
    main()

