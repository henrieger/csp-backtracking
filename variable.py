class Variable:
    def __init__(self, index: int, domain: set):
        self.index = index  # Index in input file
        self.value = None  # Currently set value of variable
        self.assigned = False  # If assigned value is valid
        self.domain = domain  # Set of all possible values

    def __repr__(self):
        return f"<Variable index={self.index}, domain={self.domain}, value={self.value}, assigned={self.assigned}>"
