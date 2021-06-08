import logging
import sys
from pathlib import Path
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig
from rich.logging import RichHandler
from rich import print

from blockchain import Blockchain
from consensus import ProofOfWork
from participant import Participant

from transaction import Transaction
from execution_time import MeasureTime

# noinspection PyArgumentList
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)


def get_participants(loaded_config: Union[DictConfig, ListConfig]) -> list[Participant]:
    return [Participant(participant) for participant in loaded_config.participants.initial]


def parse_instructions(instructions: ListConfig, blockchain: Blockchain, participants: list[Participant]) -> None:

    def get_participants_by_names(participants_names: list[str]) -> list[Participant]:
        return [p for p in participants if p.name in participants_names]

    for instruction in instructions:
        if 'blockchain' in instruction.get('show', ''):
            logging.info('Blockchain state:')
            logging.info('Genesis block:')
            print(blockchain.genesis_block)
            logging.info(f'Chains ({len(blockchain.participants_chains)}):')
            print(blockchain.participants_chains)
            print()

        elif tx_data := instruction.get('transaction', {}).get('create'):
            logging.info(f'Adding transaction "{tx_data.message}"... {tx_data.participants}')
            references_tuples = None
            if references := tx_data.get('references'):
                references_tuples = []
                for r in references:
                    if blockchain.get_block((r.participant,), r.block_index):
                        references_tuples.append((r.name, r.block_index, r.transaction_index))
                    else:
                        logging.error(f'Referenced block with index {r.block_index} does not exist.'
                                      f'Transaction will not be added.')
                        return None
            bc.add_transaction(participants=tuple(get_participants_by_names(tx_data.participants)),
                               transaction=Transaction(tx_data.message, references=references_tuples))

        elif block_data := instruction.get('block', {}).get('mine'):
            logging.info(f'Mining block... {block_data.block_participants}')
            for _ in range(block_data.get('times', 1)):
                with MeasureTime(f'MINE_BLOCK_{".".join(block_data.block_participants)}'):
                    bc.mine(participants=tuple(get_participants_by_names(block_data.block_participants)),
                            block_author=block_data.author)

        elif chain_data := instruction.get('delete', {}).get('chain'):
            logging.info(f'Deleting chain(s) related to {chain_data.participant}...')
            with MeasureTime(f'DELETE_SUBTREES_RELATED_TO_{chain_data.participant}'):
                bc.drop_chains(participant_name=chain_data.participant)

        else:
            logging.error(f'Invalid instruction: {instruction}')


if __name__ == '__main__':
    logging.info('Starting the program...')

    try:
        config = OmegaConf.load(Path(__file__).parent / 'config.yaml')
    except FileNotFoundError:
        logging.error("File 'config.yaml' is missing in the script directory.")
        sys.exit(1)

    logging.info('Creating participants...')
    participants = get_participants(config)

    logging.info('Creating Blockchain...')
    bc = Blockchain(consensus=ProofOfWork(), initial_participants=participants, variation=config.variation)
    print()

    parse_instructions(instructions=config.flow, blockchain=bc, participants=participants)
