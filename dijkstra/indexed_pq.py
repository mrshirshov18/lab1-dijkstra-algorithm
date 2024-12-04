class IndexedMinPQ:
    def __init__(self, size):
        """Indexed Minimum Priority Queue with a fixed size."""
        self.N = 0
        self.size = size
        self.values = [None] * (size + 1)  # 1-based indexing
        self.priorities = [None] * (size + 1)
        self.location = {}

    def is_empty(self):
        """Check if the priority queue is empty."""
        return self.N == 0

    def swim(self, k):
        """Restore heap order by swimming up."""
        while k > 1 and self.less(k, k // 2):
            self.swap(k, k // 2)
            k = k // 2

    def sink(self, k):
        """Restore heap order by sinking down."""
        while 2 * k <= self.N:
            j = 2 * k
            if j < self.N and self.less(j + 1, j):
                j += 1
            if not self.less(j, k):
                break
            self.swap(k, j)
            k = j

    def enqueue(self, value, priority):
        """Insert a new element with a given priority."""
        if self.N >= self.size:
            raise OverflowError("Priority queue is full.")

        self.N += 1
        self.values[self.N] = value
        self.priorities[self.N] = priority
        self.location[value] = self.N
        self.swim(self.N)

    def less(self, i, j):
        """Check if the priority at index i is less than at index j."""
        return self.priorities[i] < self.priorities[j]

    def swap(self, i, j):
        """Swap two elements in the heap."""
        self.values[i], self.values[j] = self.values[j], self.values[i]
        self.priorities[i], self.priorities[j] = self.priorities[j], self.priorities[i]
        self.location[self.values[i]] = i
        self.location[self.values[j]] = j

    def dequeue(self):
        """Remove and return the element with the smallest priority."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty priority queue.")

        min_value = self.values[1]
        self.swap(1, self.N)
        self.location.pop(min_value)
        self.values[self.N] = None
        self.priorities[self.N] = None
        self.N -= 1
        self.sink(1)
        return min_value

    def decrease_priority(self, value, lower_priority):
        """Decrease the priority of an existing element."""
        if value not in self.location:
            raise ValueError("Value does not exist in the queue.")
        idx = self.location[value]
        if lower_priority > self.priorities[idx]:
            raise ValueError(
                "New priority must be lower than or equal to the current priority."
            )

        self.priorities[idx] = lower_priority
        self.swim(idx)
