"""
XORShift Random Number Generator

Implements a configurable XORShift32 generator.
Fast, lightweight, and deterministic.
"""

class XORShiftRNG:
    def __init__(self, seed: int, *, q: int = 13, r: int = 17, s: int = 5):

        if seed == 0:
            raise ValueError("Seed must be non-zero")

        self.state = seed & 0xFFFFFFFF  # 32-bit state
        self.q = q
        self.r = r
        self.s = s

    def next(self) -> int:
        """
        Generate the next random 32-bit unsigned integer.
        """
        x = self.state
        x ^= (x << self.q) & 0xFFFFFFFF
        x ^= (x >> self.r)
        x ^= (x << self.s) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def random(self) -> float:
        """
        Generate a random float in the range [0, 1).
        """
        return self.next() / 2**32

    def randint(self, low: int, high: int) -> int:
        """
        Generate a random integer in the range [low, high].
        """
        if low > high:
            raise ValueError("low must be <= high")
        return low + self.next() % (high - low + 1)

    def generate_sequence(self, n: int, *, scale: bool = True):
        """
        Generate a random integers sequence with min-max scaling (optional).
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
    rng = XORShiftRNG(seed=123456, q=13, r=17, s=5)

    print("Raw random integers:")
    for _ in range(5):
        print(rng.next())

    print("\nScaled sequence [0, 1]:")
    scaled_seq = rng.generate_sequence(10)
    for x in scaled_seq:
        print(x)

    print("\nRandom integers between 10 and 20:")
    for _ in range(5):
        print(rng.randint(10, 20))
