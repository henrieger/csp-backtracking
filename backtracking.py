from variable import Variable
from constraint import Constraint
from typing import List
from collections import deque


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

        self.gac_3()

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

    def review_gac(self, c: Constraint, index: int):
        vars_in_scope = c.vars_in_scope(self.variables)
        x = vars_in_scope[index]

        consistent = True

        for value in x.domain:
            tuples = (t for t in c.valid_tuples if t[index] == value)
            value_consistent = False
            for t in tuples:
                for i, y in enumerate(t):
                    if y not in vars_in_scope[i].domain:
                        break
                    value_consistent = True
                    break

            if not value_consistent:
                x.domain.remove(value)
                consistent = False

        return consistent

    def gac_3(self):
        stack = deque()
        for c in self.constraints:
            for x in c.scope:
                stack.append((c, x))

        while len(stack) > 0:
            c, x = stack.pop()
            consistent = self.review_gac(c, x)

            if not consistent:
                review_constraints = (con for con in self.constraints if x in con.scope)
                for c in review_constraints:
                    for y in (var for var in c.scope if var != x):
                        stack.append((c, y))
