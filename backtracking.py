from variable import Variable
from constraint import Constraint
from typing import List


def backtracking(variables: List[Variable], constraints: List[Constraint]) -> bool:
    return backtracking_index(0, variables, constraints)


def backtracking_index(
    index: int, variables: List[Variable], constraints: List[Constraint]
) -> bool:

    if not check_restrictions(variables, constraints):
        return False

    if index >= len(variables):
        return True

    variables[index].assigned = True

    for value in variables[index].domain:
        variables[index].value = value
        if backtracking_index(index + 1, variables, constraints):
            return True

    variables[index].assigned = False
    return False


def check_restrictions(
    variables: List[Variable], constraints: List[Constraint]
) -> bool:
    for restriction in constraints:
        if not restriction.is_satisfied(variables):
            return False
    return True
