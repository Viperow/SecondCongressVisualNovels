import asyncio
from Agents import Manus


async def main():
    manus = Manus()
    while 1:
        user_input = input("请输入：")
        print(await manus.GetResponse(user_input))
if __name__ == "__main__":
    asyncio.run(main())
    
    