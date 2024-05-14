from variable import Variable
from typing import List, Dict


class Restriction:
    def __init__(self, inverted: bool, scope: List[int], valid_values: List[Dict]):
        self.inverted = inverted
        self.scope = scope
        self.valid_values = valid_values

    def is_satisfied(self, variables: list) -> bool:
        vars_in_restriction = [var for var in variables if self.var_in_scope(var)]
        if self.inverted:
            return self.__is_satisfied_inverted(vars_in_restriction)
        else:
            return self.__is_satisfied_normal(vars_in_restriction)

    def __is_satisfied_normal(self, variables: list) -> bool:
        for valid_tuple in self.valid_values:
            if self.__tuple_satisfied_normal(variables, valid_tuple):
                return True
        return False

    def __is_satisfied_inverted(self, variables: list) -> bool:
        for valid_tuple in self.valid_values:
            if self.__tuple_satisfied_inverted(variables, valid_tuple):
                return False
        return True

    def __tuple_satisfied_normal(self, variables: list, valid_tuple: dict):
        for var in variables:
            if var.assigned and valid_tuple[var.index] != var.value:
                return False
        return True

    def __tuple_satisfied_inverted(self, variables: list, valid_tuple: dict):
        for var in variables:
            if not var.assigned:
                return False
            if valid_tuple[var.index] != var.value:
                return False
        return True

    def var_in_scope(self, variable: Variable) -> bool:
        return variable.index in self.scope

    def __repr__(self):
        return f"<Restriction inverted={self.inverted}, scope={self.scope}, valid_values={self.valid_values}>"
