import aiohttp
import pytest

async def fetch(session):
    async with session.get('https://test.deribit.com/api/v2/public/ticker', params={'instrument_name':f'BTC-PERPETUAL'}) as response:
        return response.status
    
@pytest.mark.asyncio
async def test_main():
    async with aiohttp.ClientSession() as session:
        status = await fetch(session)
        assert status == 200