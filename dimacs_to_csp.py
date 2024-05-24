from sys import argv

if len(argv) != 2:
    print("Usage: python dimacs_to_text.py <DIMACS_FILE>")
    quit()

with open(argv[1]) as f:
    lines = f.readlines()

# Remove comments
lines = [line for line in lines if not line.startswith("c")]

if not lines[0].startswith("p cnf"):
    print("Error: no header 'p cnf' as first valid line of file")
    quit()

# Read first line with header
values = lines[0].split()[2:]
num_vars = int(values[0])  # Number of variables in the problem
qtd_claus = int(values[1])  # Number of clauses in the problem

print(num_vars)

# Every variable can only be TRUE of FALSE
for i in range(num_vars):
    print("2 0 1")

print(qtd_claus)


# Return binary padded version of number
def binary(i: int, digits: int) -> str:
    return " ".join(list(str(bin(i))[2:].rjust(digits, "0")))


# Generate all valid tuples for each restriction
def generate_tuples(vars):
    var = vars[0]
    positive_value = 1 if var > 0 else 0
    negative_value = 1 - positive_value
    digits = len(vars) - 1

    if len(vars) == 1:
        yield str(positive_value)
        return

    for i in range(0, 2 ** (len(vars) - 1), 1):
        yield f"{positive_value} {binary(i, digits)}"

    yield from (f"{negative_value} {t}" for t in generate_tuples(vars[1:]))


# For all restrictions
for line in lines[1:]:
    print("V")  # They are always positive restrictions

    # Print the vars involved in restriction
    vars = [int(var) for var in line.split()[:-1] if var != 0]
    print(len(vars), end=" ")
    for var in vars:
        print(abs(var), end=" ")
    print()

    # Print all valid tuples for the restriction
    num_tuples = 2 ** (len(vars)) - 1
    print(num_tuples, end=" ")
    for t in generate_tuples(vars):
        print(t, end=" ")
    print()
