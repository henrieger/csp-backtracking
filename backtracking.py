from variable import Variable
from constraint import Constraint
from typing import List
from collections import deque
from copy import deepcopy


class Backtracker:
    def __init__(self, variables: List[Variable], constraints: List[Constraint]):
        self.variables = variables
        self.constraints = constraints

    def solve(self):
        yield from self.__solve_recursive(deepcopy(self.variables), 0)

    def __solve_recursive(self, variables, index: int):
        if not self.all_constraints_satisfied():
            return

        if index >= len(variables):
            yield [var.value() for var in variables]
            return

        self.gac_3(variables)

        variable = variables[index]
        old_domain = variable.domain

        for value in old_domain:
            variable.domain = set([value])
            yield from self.__solve_recursive(deepcopy(variables), index + 1)

    def all_constraints_satisfied(self) -> bool:
        for constraint in self.constraints:
            if not constraint.is_satisfied(self.variables):
                return False
        return True

    def review_gac(self, variables: List[Variable], c: Constraint, index: int):
        vars_in_scope = c.vars_in_scope(variables)
        x = [v for v in vars_in_scope if v.index == index][0]

        consistent = True
        new_domain = x.domain.copy()

        for value in x.domain:
            tuple_index = c.get_tuple_index(index)
            tuples = (t for t in c.valid_tuples if t[tuple_index] == value)
            value_consistent = False
            for t in tuples:
                for i, y in enumerate(t):
                    if y not in vars_in_scope[i].domain:
                        break
                    value_consistent = True
                    break

            if not value_consistent:
                new_domain.remove(value)
                consistent = False

        x.domain = new_domain
        return consistent

    def gac_3(self, variables: List[Variable]):
        stack = deque()
        for c in self.constraints:
            for x in c.scope:
                stack.append((c, x))

        while len(stack) > 0:
            c, x = stack.pop()
            consistent = self.review_gac(variables, c, x)

            if not consistent:
                review_constraints = (con for con in self.constraints if x in con.scope)
                for c in review_constraints:
                    for y in (var for var in c.scope if var != x):
                        stack.append((c, y))
