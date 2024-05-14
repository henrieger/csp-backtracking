class Variable:
    def __init__(self, index: int, domain: set):
        self.index = index
        self.value = None
        self.assigned = False
        self.domain = domain

    def __repr__(self):
        return f"<Variable index={self.index}, domain={self.domain}, value={self.value}, assigned={self.assigned}>"
