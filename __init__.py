import asyncio
import threading

from dotenv import load_dotenv
load_dotenv()

from src import Registered


def start_registered():
    """
    启动注册任务
    """
    asyncio.run(Registered())

def start_registered_in_thread():
    """
    在单独的线程中启动注册任务
    """
    thread = threading.Thread(target=start_registered, daemon=True)
    thread.start()

# 在导入时自动启动任务
start_registered_in_thread()