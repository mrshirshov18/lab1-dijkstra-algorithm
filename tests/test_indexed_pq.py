import unittest
from dijkstra.indexed_pq import IndexedMinPQ


class TestIndexedMinPQ(unittest.TestCase):
    def test_enqueue_dequeue(self):
        pq = IndexedMinPQ(5)
        pq.enqueue("a", 5)
        pq.enqueue("b", 3)
        pq.enqueue("c", 4)
        pq.enqueue("d", 1)
        pq.enqueue("e", 2)

        self.assertEqual(pq.dequeue(), "d")
        self.assertEqual(pq.dequeue(), "e")
        self.assertEqual(pq.dequeue(), "b")
        self.assertEqual(pq.dequeue(), "c")
        self.assertEqual(pq.dequeue(), "a")

        with self.assertRaises(IndexError):
            pq.dequeue()

    def test_decrease_priority(self):
        pq = IndexedMinPQ(3)
        pq.enqueue("x", 10)
        pq.enqueue("y", 20)
        pq.enqueue("z", 30)

        pq.decrease_priority("z", 5)
        self.assertEqual(pq.dequeue(), "z")
        pq.decrease_priority("y", 1)
        self.assertEqual(pq.dequeue(), "y")
        self.assertEqual(pq.dequeue(), "x")

    def test_decrease_priority_to_equal(self):
        pq = IndexedMinPQ(2)
        pq.enqueue("p", 15)
        pq.enqueue("q", 15)

        pq.decrease_priority("q", 15)
        self.assertEqual(pq.dequeue(), "p")
        self.assertEqual(pq.dequeue(), "q")

    def test_decrease_priority_invalid(self):
        pq = IndexedMinPQ(1)
        pq.enqueue("s", 50)

        with self.assertRaises(ValueError):
            pq.decrease_priority("s", 60)  # New priority higher than current

        with self.assertRaises(ValueError):
            pq.decrease_priority("nonexistent", 10)  # Value not in queue

    def test_overflow(self):
        pq = IndexedMinPQ(2)
        pq.enqueue("a", 1)
        pq.enqueue("b", 2)
        with self.assertRaises(OverflowError):
            pq.enqueue("c", 3)

    def test_is_empty(self):
        pq = IndexedMinPQ(1)
        self.assertTrue(pq.is_empty())
        pq.enqueue("a", 1)
        self.assertFalse(pq.is_empty())
        pq.dequeue()
        self.assertTrue(pq.is_empty())

    def test_duplicate_priorities(self):
        pq = IndexedMinPQ(3)
        pq.enqueue("a", 5)
        pq.enqueue("b", 5)
        pq.enqueue("c", 5)
        dequeued_elements = [pq.dequeue(), pq.dequeue(), pq.dequeue()]
        self.assertCountEqual(dequeued_elements, ["a", "b", "c"])

    def test_same_priority_decrease(self):
        pq = IndexedMinPQ(2)
        pq.enqueue("a", 5)
        pq.enqueue("b", 5)
        pq.decrease_priority("b", 5)
        self.assertEqual(pq.dequeue(), "a")
        self.assertEqual(pq.dequeue(), "b")


if __name__ == "__main__":
    unittest.main()
