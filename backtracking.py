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
        yield from self.__solve_recursive(self.__sort_by_domain(self.variables), 0)

    def __solve_recursive(self, variables, index: int):
        if not self.all_constraints_satisfied(variables):
            return

        if index >= len(variables):
            yield [var.value() for var in self.__sort_by_index(variables)]
            return

        self.gac_3(variables)
        for v in variables:
            if len(v.domain) == 0:
                return

        variable = variables[index]
        old_domain = variable.domain

        for value in old_domain:
            variable.domain = set([value])
            yield from self.__solve_recursive(
                self.__sort_by_domain(variables), index + 1
            )

    def all_constraints_satisfied(self, variables) -> bool:
        for constraint in self.constraints:
            if not constraint.is_satisfied(self.__sort_by_index(variables)):
                return False
        return True

    def review_gac(self, variables: List[Variable], c: Constraint, index: int):
        ordered_variables = self.__sort_by_index(variables)
        vars_in_scope = c.vars_in_scope(ordered_variables)
        x = [v for v in vars_in_scope if v.index == index][0]

        consistent = True

        for value in x.domain:
            value_consistent = c.value_consistent(index-1, value, ordered_variables)

            if not value_consistent:
                consistent = False

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

    def __sort_by_domain(self, variables: List[Variable]) -> List[Variable]:
        new_variables = deepcopy(variables)
        return sorted(new_variables, key=lambda x: len(x.domain))

    def __sort_by_index(self, variables: List[Variable]) -> List[Variable]:
        return sorted(variables, key=lambda x: x.index)
