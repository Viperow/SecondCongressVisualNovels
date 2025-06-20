import asyncio
from Agents import Manus

async def main():
    manus = Manus()
    await manus.run("选举李大钊为委员")

if __name__ == "__main__":
    asyncio.run(main())
    
    