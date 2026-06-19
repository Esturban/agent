import asyncio


async def fetch_weather() -> str:
    """Simulate a 1-second weather API call."""
    await asyncio.sleep(1)
    return "Sunny, 22 C"


async def fetch_news() -> str:
    """Simulate a 1-second news API call."""
    await asyncio.sleep(1)
    return "Markets up 0.3%"


async def fetch_calendar() -> str:
    """Simulate a 1-second calendar API call."""
    await asyncio.sleep(1)
    return "3 meetings today"


async def fetch_stock() -> str:
    """Simulate a 1-second stock API call."""
    await asyncio.sleep(1)
    return "AAPL +1.2%"
