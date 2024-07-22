from variable import Variable
from constraint import Constraint
from typing import List


class Backtracker:
    def __init__(self, variables: List[Variable], constraints: List[Constraint]):
        self.variables = variables
        self.constraints = constraints

    def solve(self):
        yield from self.__solve_recursive(0)

    def __solve_recursive(self, index: int):
        if not self.all_constraints_satisfied():
            return

        if index >= len(self.variables):
            yield [var.value() for var in self.variables]
            return

        variable = self.variables[index]
        old_domain = variable.domain

        for value in old_domain:
            variable.domain = set([value])
            yield from self.__solve_recursive(index + 1)

        variable.domain = old_domain

    def all_constraints_satisfied(self) -> bool:
        for constraint in self.constraints:
            if not constraint.is_satisfied(self.variables):
                return False
        return True
