#
# UPQueue.py -- an updatable priority queue structure
# A. Thall
# CSC 345 F18
# 10/5/18
#
# Updatable priority queues are used in many path-finding algorithms
# This one uses a min-heap structure along with a hashed dict index-list
# over item-keys.
# Adding an item takes a (key, item, priority) triple, heapifies the
#   item to its priority position in the min-heap, and stores its location
#   in the minheap indexed by key value in a dictionary.
#
# Usage:  myQ = UPQueue
#         myQ.insert((2, 1), "Samson", 3)
#

class UPQueue:

    def __init__(self):

        self.indices = {}
        self.heap = [None]

    def insert(self, key, item, priority):
        dex = len(self.heap)
        self.indices[key] = dex
        self.heap.append([key, item, priority])
        self.__decrease_key(dex)

    def get_priority(self, key):
        i = self.indices[key]
        return self.heap[i][2]

    def reduce_priority(self, key, priority):
        i = self.indices[key]
        self.heap[i][2] = priority
        self.__decrease_key(i)

    def replace(self, key, item, priority):
        """
        This puppy is non-standard, uses key to find item
        and change its value and priority.  It then adjusts position
        in heap appropriately.  This is in cases where state of object
        has been changed along with changing priority
        """
        i = self.indices[key]
        self.heap[i][1] = item
        self.heap[i][2] = priority
        # could check to see if need to raise or lower
        self.__decrease_key(i)
        self.min_heapify(i)

    def __decrease_key(self, i):
        """
        Don't accidently try to use this to reduce the priority.
        This is strictly for building and maintaining the heap.
        Let's make it private
        """
        A = self.heap
        while i > 1 and A[i//2][2] > A[i][2]:
            A[i//2], A[i] = A[i], A[i//2]
            self.indices[A[i][0]] = i
            self.indices[A[i//2][0]] = i//2
            i = i//2

    def empty(self):
        return len(self) == 0

    def __len__(self):
        return len(self.heap) - 1

    def __contains__(self, key):
        return key in self.indices

    def __str__(self):
        return "len(heap) = %d\nindices = %s\n heap = %s" % (len(self), str(self.indices), str(self.heap))

    def remove_min(self):
        """
        Remove the minimum element and then reheapify
        :return:  tuple with element and final priority
        """
        if len(self) == 0:
            # xxAT should maybe throw exception here
            return None
        elif len(self) == 1:
            # pop last remaining item and clear indices
            node = self.heap.pop()
            self.indices.clear()
            return node[1], node[2]
        else:
            node = self.heap[1]
            del self.indices[node[0]]
            self.heap[1] = self.heap.pop()
            self.indices[self.heap[1][0]] = 1
            self.min_heapify(1)
            return node[1], node[2]

    def min_heapify(self, i):
        A = self.heap
        l = 2*i
        r = 2*i + 1
        if l <= len(self) and A[l][2] < A[i][2]:
            smallest = l
        else:
            smallest = i
        if r <= len(self) and A[r][2] < A[smallest][2]:
            smallest = r

        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]
            self.indices[A[i][0]] = i
            self.indices[A[smallest][0]] = smallest
            self.min_heapify(smallest)
