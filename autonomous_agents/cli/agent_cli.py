from autonomous_agents.main import AgentSystem
import click
import asyncio


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug):
    """Run the autonomous agents system."""
    if debug:
        from ..utils.logger import logger
        logger.setLevel("DEBUG")
    
    system = AgentSystem()
    asyncio.run(system.main())