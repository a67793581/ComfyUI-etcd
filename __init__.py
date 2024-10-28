import asyncio

from dotenv import load_dotenv
load_dotenv()

from src import Registered
asyncio.run(Registered())


