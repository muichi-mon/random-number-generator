"""
Linear Congruential Generator (LCG)

Implements a configurable LCG for generating pseudo-random numbers.
Fast, lightweight, and deterministic.
"""

class LCG:
    def __init__(self, seed: int, *, a: int = 1664525, c: int = 1013904223, m: int = 2**32):
        """
        Initialize the LCG with parameters:
        X_{n+1} = (a * X_n + c) % m
        """
        if seed == 0:
            raise ValueError("Seed must be non-zero")
        self.state = seed % m
        self.a = a
        self.c = c
        self.m = m

    def next(self) -> int:
        """
        Generate the next random integer in [0, m-1].
        """
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def random(self) -> float:
        """
        Generate a random float in [0, 1).
        """
        return self.next() / self.m

    def randint(self, low: int, high: int) -> int:
        """
        Generate a random integer in [low, high].
        """
        if low > high:
            raise ValueError("low must be <= high")
        return low + self.next() % (high - low + 1)

    def generate_sequence(self, n: int, *, scale: bool = True):
        """
        Generate a sequence of n integers.
        If scale=True, scale to [0, 1] using min-max scaling.
        """
        if n <= 0:
            raise ValueError("n must be positive")
        seq = [self.next() for _ in range(n)]
        if not scale:
            return seq

        min_val = min(seq)
        max_val = max(seq)
        if max_val == min_val:
            return [0.0 for _ in seq]
        return [(x - min_val) / (max_val - min_val + 1e-6) for x in seq]


# Example usage
if __name__ == "__main__":
    lcg = LCG(seed=123456)

    print("Raw random integers:")
    for _ in range(5):
        print(lcg.next())

    print("\nScaled sequence [0, 1]:")
    scaled_seq = lcg.generate_sequence(10)
    for x in scaled_seq:
        print(x)

    print("\nRandom integers between 10 and 20:")
    for _ in range(5):
        print(lcg.randint(10, 20))
