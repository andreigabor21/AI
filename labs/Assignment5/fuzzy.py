class Fuzzyfier:
    def __init__(self, left: int, right: int, mean=None):
        self._left = left
        self._right = right
        self._mean = mean
        if self._mean is None:
            self._mean = (self._left + self._right) / 2

    def compute_fuzzy_triangle(self, x: float) -> float:
        if self._left is not None and self._left <= x < self._mean:
            return (x - self._left) / (self._mean - self._left)
        elif self._right is not None and self._mean <= x < self._right:
            return (self._right - x) / (self._right - self._mean)
        else:
            return 0