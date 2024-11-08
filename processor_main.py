"""Entry point for the transfer processor."""
import asyncio
import signal

from autonomous_agents.utils.transfer_prcessor import TransferProcessor


async def main():
    processor = TransferProcessor()
    
    # Setup signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(processor.shutdown())
        )
    
    await processor.run()

if __name__ == "__main__":
    asyncio.run(main())