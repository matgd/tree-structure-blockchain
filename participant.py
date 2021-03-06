class Participant:
    def __init__(self, name: str):
        self.name = name
        self.deleted = False

    def __repr__(self) -> str:
        return f'Participant({self.name})'

    def __str__(self) -> str:
        return f'P({self.name})'
