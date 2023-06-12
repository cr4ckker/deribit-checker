import json, time
import uvicorn

from fastapi import FastAPI, Response

from db import *

app = FastAPI()
app.debug = True

@app.route('/get_info')
async def get_info(request):
    ticker = request.query_params.get('ticker', 'BTC')
    with Session(engine) as session:
        items = session.execute( select(Price)
                                .where(Price.ticker == ticker)
                                ).all()
    return Response(json.dumps([ item[0]._jsonify() for item in items ]))

@app.route('/get_price')
async def get_price(request):
    ticker = request.query_params.get('ticker', 'BTC')
    with Session(engine) as session:
        item = session.execute( select( Price.price )
                                .where( Price.ticker == ticker )
                                .order_by( Price.timestamp.desc() )
                                ).fetchone()
    return Response(json.dumps({ 'price': item[0] }))

@app.route('/get_price_by_date')
async def last_price(request):
    ticker = request.query_params.get('ticker', 'BTC')
    date = request.query_params.get('date')
    if not date:
        return Response(json.dumps({"error":'"date" parameter is missing'}), 400)
    with Session(engine) as session:
        items = session.execute( select( Price.timestamp, Price.price )
                                .where( Price.ticker == ticker
                                       and time.strftime(r'%d.%m.%Y', Price.timestamp) == time.strftime(r'%d.%m.%Y', date) )
                                ).fetchall()
    return Response(json.dumps({ item[0]: item[1] for item in items }))

uvicorn.run(app, port=5021)
