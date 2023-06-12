import aiohttp, asyncio, time

from db import *

tickers = ['BTC', 'ETH']

async def fetch(session, ticker):
    async with session.get('https://test.deribit.com/api/v2/public/ticker', params={'instrument_name':f'{ticker}-PERPETUAL'}) as response:
        response = await response.json()
        with Session(engine) as session:
            response_price = response['result']['best_ask_price']
            session.add(Price(ticker=ticker, price=response_price, timestamp=time.time()))
            session.commit()

async def main():
    while True:
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[fetch(session, ticker) for ticker in tickers])
        await asyncio.sleep(60)


asyncio.get_event_loop().run_until_complete(main())