from variable import Variable
from typing import List, Tuple
from itertools import product


class Constraint:
    def __init__(
        self,
        negative: bool,
        scope: list,
        valid_tuples: List[Tuple],
    ):
        self.negative = negative
        self.valid_tuples = valid_tuples
        self.scope = sorted(scope)

    # Check if restriction is satisfied
    def is_satisfied(self, variables: list) -> bool:
        domains = (var.domain for var in variables if var.index in self.scope)
        all_tuples = set(tuple(values) for values in product(*domains))

        tuples = self.valid_tuples
        if self.negative:
            tuples = all_tuples - tuples

        return bool(all_tuples & tuples)

    def __repr__(self):
        return f"<Constraint scope={self.scope} tuples={self.valid_tuples}>"
