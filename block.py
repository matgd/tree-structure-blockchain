from datetime import datetime
from hashlib import sha256
import json
from typing import Optional, Union

from participant import Participant
from transaction import Transaction

from copy import deepcopy


class Block:
    def __init__(self,
                 index: int,
                 transactions: list[Transaction],
                 timestamp: datetime,
                 previous_hash: str,
                 participants: Union[tuple[Participant], tuple, None],
                 author: Optional[str],
                 nonce: int = 0):
        self.index = index
        self.transactions = str(transactions)
        self.timestamp: str = str(timestamp.isoformat())
        self.previous_hash = previous_hash
        self.participants = str(participants)
        self.author = author
        self.nonce = nonce
        self.hash = ''

    def compute_hash(self) -> str:
        content_for_hash = deepcopy(vars(self))
        content_for_hash.pop('author')
        content_for_hash.pop('hash')
        block_string = json.dumps(content_for_hash, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f'Block({vars(self)})'
