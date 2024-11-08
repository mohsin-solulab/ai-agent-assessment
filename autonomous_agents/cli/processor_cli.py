from autonomous_agents.utils.transfer_prcessor import TransferProcessor
import click
import asyncio


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug):
    """Run the transfer processor."""
    if debug:
        from ..utils.logger import logger
        logger.setLevel("DEBUG")
    
    processor = TransferProcessor()
    asyncio.run(processor.run())