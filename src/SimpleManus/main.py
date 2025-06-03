import asyncio
from Agents import Manus

async def main():
    manus = Manus()
    await manus.run("帮我总结勾股定理所需要的知识点，并询问用户满不满意，然后并写为文件")

if __name__ == "__main__":
    asyncio.run(main())
    
    