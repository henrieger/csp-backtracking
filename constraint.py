from variable import Variable
from typing import List, Tuple, Set
from itertools import product


class Constraint:
    def __init__(
        self,
        negative: bool,
        scope: list,
        tuples: List[Tuple],
    ):
        self.scope = sorted(scope)
        self.negative = negative
        self.tuples = tuples

    # Check if restriction is satisfied
    def is_satisfied(self, variables: list) -> bool:
        domains = [var.domain for var in variables if var.index in self.scope]

        def tuple_in_domains(t: tuple, domains: List[Set]):
            for i, v in enumerate(t):
                if v not in domains[i]:
                    return False
            return True

        def domains_without_tuples(tuples: Set[Tuple], domains: List[Set]):
            all_tuples = set(tuple(t) for t in product(*domains))
            return bool(all_tuples - self.tuples)

        if self.negative:
            return domains_without_tuples(self.tuples, domains)

        else:
            for t in self.tuples:
                if tuple_in_domains(t, domains):
                    return True
            return False

    # Get Variable objects of all variables in restriction, in order
    def vars_in_scope(self, variables: List[Variable]):
        return [v for v in variables if v.index in self.scope]

    def get_tuple_index(self, index: int):
        return self.scope.index(index)

    def value_consistent(self, index: int, value, variables: List[Variable]):
        if index not in self.scope:
            return True

        old_domain = variables[index].domain
        variables[index].domain = set([value])
        if self.is_satisfied(variables):
            variables[index].domain = old_domain
            return True

        variables[index].domain = old_domain - set([value])
        return False

    def __repr__(self):
        return f"<Constraint negative={self.negative} scope={self.scope} tuples={self.tuples}>"
