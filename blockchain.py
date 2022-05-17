import logging
from datetime import datetime
from enum import Enum
from itertools import combinations
from typing import Optional, Union

from block import Block
from consensus import Consensus
from execution_time import MeasureTime
from participant import Participant
from transaction import Transaction


class BlockchainVariation(Enum):
    NONE = 'NONE'
    REFERENCE = 'REFERENCE'


class Blockchain:
    def __init__(self, consensus: Consensus, initial_participants: list[Participant], variation: str):
        self.participants_chains = {combination: [] for combination
                                    in self.__get_all_participants_combinations(initial_participants)}
        self.participants_pending_transactions = {combination: [] for combination
                                                  in self.__get_all_participants_combinations(initial_participants)}
        self.participants = initial_participants
        self.variation = BlockchainVariation(variation)
        logging.debug('Blockchain:')
        logging.debug(f'{self.participants_chains=}')
        logging.debug(f'{len(self.participants_chains)=}')
        self.consensus = consensus
        self.genesis_block = None
        self.configure()

    def configure(self) -> None:
        self.genesis_block = self.__create_genesis_block()

    @staticmethod
    def __get_all_participants_combinations(participants: list[Participant]) -> list[tuple[Participant]]:
        return [combination for i in range(len(participants))
                for combination in combinations(participants, i + 1)] + [()]  # + empty set as tuple

    def __create_genesis_block(self) -> Block:
        # TODO: Generate genesis block with respecting PoW difficulty
        if self.genesis_block is not None:
            logging.warning('Creating genesis block despite it is already created...')
        genesis_block = Block(index=0,
                              transactions=[],
                              timestamp=datetime.utcnow(),
                              previous_hash='0',
                              participants=None,
                              author=None)
        genesis_block = self.consensus.mine(genesis_block)
        logging.debug(f'{genesis_block=}')
        return genesis_block

    def __get_participant_by_name(self, name: str) -> Optional[Participant]:
        for p in self.participants:
            if p.name == name:
                return p
        return None

    @staticmethod
    def __mark_participant_as_deleted(participant: Participant) -> None:
        # Here could be additional instructions for cleaning participant's data
        participant.name = f"{participant.name}'"
        participant.deleted = True

    def append_block(self, block: Block, participants: Union[tuple[Participant], tuple],
                     previous_block_hash: str) -> bool:
        if previous_block_hash != block.previous_hash:
            logging.error(f'Cannot append new block {previous_block_hash=}, {block.previous_hash=}.')
            return False
        if not self.consensus.validate_hash(block):
            logging.error(f'Cannot append new block as it does not meet required hash {block.hash=}.')
            return False

        self.participants_chains[participants].append(block)
        return True

    def get_block(self, participants_names: Union[tuple[str], tuple], index: int) -> Optional[Block]:
        # Index is the position of block in sub-chain list
        try:
            subchain_key = tuple([self.__get_participant_by_name(pn) for pn in participants_names])
            return self.participants_chains[subchain_key][index-1]
        except KeyError:
            logging.error('Invalid participants set.')
        except IndexError:
            logging.error('Block with given index does not exist.')
        return None

    def add_transaction(self, participants: Union[tuple[Participant], tuple], transaction: Transaction) -> None:
        self.participants_pending_transactions[participants].append(transaction)

    def drop_chains(self, participant_name: str) -> bool:
        if not (participant_to_leave := self.__get_participant_by_name(participant_name)):
            logging.warning(f'Could not find participant by name {participant_name}. Chain(s) will not be deleted.')
            return False
        related_chain_keys = [chain_key for chain_key in self.participants_chains if participant_to_leave in chain_key]

        with MeasureTime(f'DELETE_SUBTREE_{participant_name}'):
            if self.variation == BlockchainVariation.NONE:
                for chain_key in related_chain_keys:
                    self.participants_chains.pop(chain_key)
                    self.participants_pending_transactions.pop(chain_key)
                return True
            elif self.variation == BlockchainVariation.REFERENCE:
                self.__mark_participant_as_deleted(participant_to_leave)
                for chain_key in related_chain_keys:
                    if all((participant.deleted for participant in chain_key)):
                        with MeasureTime(f'DELETE_CHAIN_{str(chain_key).replace(",", "_")}'):
                            self.participants_chains.pop(chain_key)
                return True

    def mine(self, participants: Union[tuple[Participant], tuple],
             block_author: Optional[str] = None) -> None:
        if not self.participants_pending_transactions[participants]:
            logging.warning(f'No pending transactions for {participants=}. Block will be mined without transactions.')
        previous_block = self.participants_chains[participants][-1] \
            if self.participants_chains[participants] else self.genesis_block

        new_block = Block(index=previous_block.index + 1,
                          transactions=self.participants_pending_transactions
                            [participants],
                          timestamp=datetime.utcnow(),
                          previous_hash=previous_block.hash,
                          participants=participants,
                          author=block_author)

        self.append_block(block=self.consensus.mine(new_block),
                          participants=participants,
                          previous_block_hash=previous_block.hash)

        self.participants_pending_transactions[participants] = []
