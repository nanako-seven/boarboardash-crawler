from models import init_database
import asyncio

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(init_database())
    loop.close()
