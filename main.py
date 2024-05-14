from variable import Variable
from restriction import Restriction
from backtracking import backtracking


def main():
    variable_amount = int(input())
    variables = []

    for index in range(1, variable_amount+1):
        domain_tokens = input().split()
        domain_size = int(domain_tokens[0])
        domain = set()
        for i in range(1, domain_size+1):
            domain.add(int(domain_tokens[i]))
        variables.append(Variable(index, domain))

    restriction_amount = int(input())
    restrictions = []

    for _ in range(restriction_amount):
        inverted = (input().lower() == 'i')
        scope_tokens = input().split()
        scope_size = int(scope_tokens[0])
        scope = []

        for i in range(1, scope_size+1):
            scope.append(int(scope_tokens[i]))

        tuple_tokens = input().split()
        tuple_amount = int(tuple_tokens[0])
        tuples = []

        for i in range(tuple_amount):
            valid = {}
            for j in range(scope_size):
                valid[scope[j]] = int(tuple_tokens[scope_size * i + j + 1])
            tuples.append(valid)
        restrictions.append(Restriction(inverted, scope, tuples))

    if backtracking(variables, restrictions):
        for variable in variables:
            print(f"x{variable.index} = {variable.value}")
    else:
        print("INVIAVEL")


if __name__ == "__main__":
    main()
