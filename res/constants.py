from res import id as id
import os

# url
url = {
    id.ws_candles: 'wss://api.bitfinex.com/ws/2'
}

#channel subscribe
subscribe = {
    id.ws_subscribe: '"event": "subscribe",  "channel": "candles",  "key": "trade:{}:t{}"'
}

#coin list
coinbase = [
    "ioteth", "iotbtc", "btcusd", "ltcusd", "ltcbtc", "ethusd", "ethbtc", "etcbtc", "etcusd", "rrtusd", "rrtbtc",
    "zecusd", "zecbtc", "xmrusd", "xmrbtc", "dshusd", "dshbtc", "btceur", "btcjpy", "xrpusd", "iotusd", "eosusd",
]

#time frame
time_frame = [ '5m', '30m', '1h', '3h', '6h', '12h', '1d' ]
