from variable import Variable
from constraint import Constraint
from typing import List


class Backtracker:
    def __init__(self, variables: List[Variable], constraints: List[Constraint]):
        self.variables = variables
        self.constraints = constraints

    def solve(self):
        yield from self.__solve(0)

    def __solve(self, index: int):
        if not self.all_constraints_satisfied():
            return

        if index >= len(self.variables):
            yield [var.value for var in self.variables]
            return

        self.variables[index].assigned = True

        for value in self.variables[index].domain:
            self.variables[index].value = value
            yield from self.__solve(index + 1)

        self.variables[index].assigned = False

    def all_constraints_satisfied(self) -> bool:
        for constraint in self.constraints:
            if not constraint.is_satisfied(self.variables):
                return False
        return True
