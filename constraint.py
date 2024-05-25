from variable import Variable
from typing import List, Dict


class Constraint:
    def __init__(self, negative: bool, valid_values: List[Dict]):
        self.negative = negative  # If tuple values should be treated as negative constraints
        self.valid_values = valid_values  # Valid values for each of the variables

    # Generate an iter of variables present in the scope of constraint
    def scope(self) -> list:
        return self.valid_values[0].keys()

    # Check if restriction is satisfied
    def is_satisfied(self, variables: list) -> bool:
        vars_in_restriction = [var for var in variables if self.var_in_scope(var)]
        if self.negative:
            return self.__is_satisfied_inverted(vars_in_restriction)
        else:
            return self.__is_satisfied_normal(vars_in_restriction)

    # Check if a positive constraint is satisfied
    def __is_satisfied_normal(self, variables: list) -> bool:
        for valid_tuple in self.valid_values:
            if self.__tuple_satisfied_normal(variables, valid_tuple):
                return True
        return False

    # Check if a negative constraint is satisfied
    def __is_satisfied_inverted(self, variables: list) -> bool:
        for valid_tuple in self.valid_values:
            if self.__tuple_satisfied_inverted(variables, valid_tuple):
                return False
        return True

    # Check if a tuple of a positive constraint is satisfied
    def __tuple_satisfied_normal(self, variables: list, valid_tuple: dict):
        for var in variables:
            if var.assigned and valid_tuple[var.index] != var.value:
                return False
        return True

    # Check if a tuple of a negative constraint is satisfied
    def __tuple_satisfied_inverted(self, variables: list, valid_tuple: dict):
        for var in variables:
            if not var.assigned or valid_tuple[var.index] != var.value:
                return False
        return True

    # Check if variable is in scope of restriction
    def var_in_scope(self, variable: Variable) -> bool:
        return variable.index in self.scope()

    def __repr__(self):
        return f"<Restriction inverted={self.negative}, scope={self.scope}, valid_values={self.valid_values}>"
