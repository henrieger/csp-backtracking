class Variable:
    def __init__(self, index: int, domain: set):
        self.index = index  # Index in input file
        self.domain = domain  # Set of all possible values

    def __repr__(self):
        return f"<Variable index={self.index}, domain={self.domain}>"

    def assigned(self) -> bool:
        return len(self.domain) == 1

    def value(self):
        if self.assigned():
            return next(iter(self.domain))
        return None
