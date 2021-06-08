from abc import ABC, abstractmethod

from block import Block


class Consensus(ABC):
    @abstractmethod
    def mine(self, block: Block, **kwargs) -> Block:
        pass

    @abstractmethod
    def validate_hash(self, block: Block, **kwargs) -> bool:
        pass


class ProofOfWork(Consensus):
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty

    def mine(self, block: Block, **kwargs) -> Block:
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        block.hash = computed_hash
        return block

    def validate_hash(self, block: Block, **kwargs) -> bool:
        return block.hash == block.compute_hash()
