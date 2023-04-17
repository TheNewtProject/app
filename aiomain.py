import asyncio
import importlib
from framework import newt as fw
from framework import plugins

async def main():
    app = fw.Newt()
    await app.run_async()

asyncio.run(main())