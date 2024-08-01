#!/usr/bin/python3
from variable import Variable
from constraint import Constraint
from backtracking import Backtracker
from sys import argv, stdin


def main():
    # Read input file
    file = stdin
    if len(argv) == 2:
        file = open(argv[1], "r")
    lines = file.readlines()
    file.close()

    # Amount of variables in the problem described in the first line
    variable_amount = int(lines[0])
    variables = []

    # Read variable domains
    variable_domains = lines[1 : variable_amount + 1]
    for index, line in enumerate(variable_domains):
        domain_tokens = line.split()
        domain = set()
        for token in domain_tokens[1:]:
            domain.add(int(token))
        variables.append(Variable(index + 1, domain))

    # Separate constraint definitions into chunks of 3 lines
    constraint_lines = lines[variable_amount + 2 :]
    constraint_definitions = [
        constraint_lines[i : i + 3] for i in range(0, len(constraint_lines), 3)
    ]

    # Read constraints
    constraints = []
    for definition in constraint_definitions:
        # Check if constraint should be negative
        negative = definition[0].strip().lower() == "i"

        # Add variables to constraint scope
        scope_tokens = definition[1].split()
        scope_size = int(scope_tokens[0])
        scope = []
        for token in scope_tokens[1:]:
            scope.append(int(token))

        # Separate the line into "tuples"
        tuple_line = definition[2]
        tuple_tokens = tuple_line.split()
        tuple_list = [
            tuple_tokens[i : i + scope_size]
            for i in range(1, len(tuple_tokens), scope_size)
        ]

        # Create a list of dicts with tuple vars and valid values
        tuple_dicts = []
        for tuple_values in tuple_list:
            valid = {}
            for index, value in enumerate(tuple_values):
                valid[scope[index]] = int(value)
            tuple_dicts.append(valid)

        # Sort values and convert to tuples
        tuples = set(tuple(dict(sorted(t.items())).values()) for t in tuple_dicts)

        # Add constraint to list
        constraints.append(Constraint(negative, scope, tuples, variables))

    # Generate solutions
    solutions = Backtracker(variables, constraints).solve()
    has_solution = False

    # Print result of first solution
    for solution in solutions:
        has_solution = True
        for index, value in enumerate(solution):
            print(f"x{index+1} = {value}")
        return
        print()

    # If no solution was generated, problem is declared unfeasible
    # and program is aborted
    if not has_solution:
        print("INVIAVEL")


if __name__ == "__main__":
    main()
