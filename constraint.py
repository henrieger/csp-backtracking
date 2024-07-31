from variable import Variable
from typing import List, Tuple
from itertools import product


class Constraint:
    def __init__(
        self,
        negative: bool,
        scope: list,
        valid_tuples: List[Tuple],
        variables: List[Variable],
    ):
        self.scope = sorted(scope)

        if negative:
            domains = (var.domain for var in variables if var.index in self.scope)
            all_tuples = set(tuple(values) for values in product(*domains))
            self.valid_tuples = all_tuples - valid_tuples
        else:
            self.valid_tuples = valid_tuples

    # Check if restriction is satisfied
    def is_satisfied(self, variables: list) -> bool:
        domains = (var.domain for var in variables if var.index in self.scope)
        all_tuples = set(tuple(values) for values in product(*domains))

        return bool(all_tuples & self.valid_tuples)

    # Get Variable objects of all variables in restriction, in order
    def vars_in_scope(self, variables: List[Variable]):
        return [v for v in variables if v.index in self.scope]

    def get_tuple_index(self, index: int):
        return self.scope.index(index)

    def __repr__(self):
        return f"<Constraint scope={self.scope} tuples={self.valid_tuples}>"
