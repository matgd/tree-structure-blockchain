class Transaction:
    next_id = 1

    def __init__(self, content: str, references: list[tuple[str, int, int]] = None):
        # References in form of reference name, block index, transaction index
        self.id = Transaction.next_id
        self.content = content
        self.references = references
        Transaction.next_id += 1

    def __repr__(self) -> str:
        references_message = f'  REFERENCES: {self.references}' if self.references else ''
        return f'T({self.id}: {self.content}{references_message})'

    def __str__(self) -> str:
        references_message = f'  REFERENCES: {self.references}' if self.references else ''
        return f'T({self.id}: {self.content} {references_message})'
