from variable import Variable
from restriction import Restriction
from typing import List


def backtracking(variables: List[Variable], restrictions: List[Restriction]) -> bool:
    return backtracking_index(0, variables, restrictions)


def backtracking_index(
    index: int, variables: List[Variable], restrictions: List[Restriction]
) -> bool:

    if not check_restrictions(variables, restrictions):
        return False

    if index >= len(variables):
        return True

    variables[index].assigned = True

    for value in variables[index].domain:
        variables[index].value = value
        if backtracking_index(index + 1, variables, restrictions):
            return True

    variables[index].assigned = False
    return False


def check_restrictions(
    variables: List[Variable], restrictions: List[Restriction]
) -> bool:
    for restriction in restrictions:
        if not restriction.is_satisfied(variables):
            return False
    return True
