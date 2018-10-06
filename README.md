Python class UPQueue

  UPQueue.py -- an updatable priority queue structure
  (c) Andrew Thall, Alma College

  This is released under the Too-Trivial-To-Worry-About-It license.  Use it for good
  and not evil.  No guarantees of correctness, so don't use it in Mars lander
  or radiation-treatment code or anything like that.

  Tired of rewriting this class every few years in the langue du jour,
  so here it is in Python 2.7 in a public repo.

  10/5/18

  Updatable priority queues are used in many search algorithms.
  This one uses a min-heap structure along with a hashed dict index-list
  over item-keys.  This gives O(1) for key membership tests, and O(lg n)
  for insert, remove-min, and decrease-priority operations.

  Adding an item takes a (key, item, priority) triple, heapifies the
    item to its priority position in the min-heap, and stores its location
    in the minheap indexed by key value in a dictionary.

  1) The key can be anything that's legal for a dictionary.  For the A* puzzle-solver
  this was created for, it was 9-tuples representing board positions

  2) The item can be anything.

  3) The priority can be anything with ordered comparison ops

  Note:  this is not a "stable" queue; since it uses a heap, there is no
     guaranteed FIFO ordering on sequentially added items with the same priority

  See the internal documentation for usage examples.
 