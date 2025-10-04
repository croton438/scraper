"""
Sompo Login Test Script
"""
import asyncio
from portals import sompo

async def main():
    print("=" * 60)
    print("SOMPO LOGIN TEST")
    print("=" * 60)
    
    result = await sompo.login()
    
    print("\n" + "=" * 60)
    print("SONUÇ:")
    print("=" * 60)
    print(result)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

