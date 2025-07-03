import asyncio

import steamwebapi


async def main():
    async with steamwebapi.Client("SteamWebAPI Token Here") as client:
        # Use client here.
        ...


if __name__ == "__main__":
    asyncio.run(main())
