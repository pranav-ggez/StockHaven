from flask import Flask, render_template, request
import yfinance as yf
<<<<<<< HEAD
from binance.client import Client
import plotly.graph_objects as go

app = Flask(__name__)

binance = Client()

def get_usd_inr_rate():
=======

app = Flask(__name__)

def get_usd_inr_rate():
    """Fetch the latest USD/INR rate using yfinance."""
>>>>>>> 87d35b4d686ba401422d1cc51c9c027048185338
    try:
        fx = yf.Ticker("USDINR=X")
        hist = fx.history(period="1d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
<<<<<<< HEAD
    except:
        return None

def fetch_from_binance(symbol):
    try:
        symbol = symbol.upper()
        if not symbol.endswith(("USDT", "BUSD", "BTC")):
            symbol = symbol + "USDT"

        data = binance.get_ticker(symbol=symbol)
        price = float(data["lastPrice"])
        prev_price = float(data.get("prevClosePrice", 0))
        change = price - prev_price if prev_price else None
        change_percent = (change / prev_price * 100) if prev_price else None

        return {
            "name": symbol.replace("USDT", ""),
            "symbol": symbol,
            "currency": "USDT",
            "price": price,
            "marketCap": None,
            "previousClose": prev_price,
            "open": float(data.get("openPrice", 0)),
            "dayHigh": float(data.get("highPrice", 0)),
            "dayLow": float(data.get("lowPrice", 0)),
            "change": change,
            "changePercent": change_percent
        }
    except:
        return None

def generate_candles(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo", interval="1d")
        if hist.empty:
            return None

        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        return fig.to_html(full_html=False, config={"displayModeBar": False})
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    stocks = []
    primary_stock = None
    errors = []
    usd_inr_rate = None

    if request.method == "POST":
        raw = request.form.get("company", "").strip()
        if raw:
            symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]

            for sym in symbols:
                stock_data = None

                if sym.endswith(("USDT", "BTC", "ETH", "BUSD")) or len(sym) <= 5:
                    stock_data = fetch_from_binance(sym)

                if stock_data is None:
                    try:
                        ticker = yf.Ticker(sym)
                        info = ticker.info
                    except:
                        info = None

                    if not info or ("longName" not in info and "shortName" not in info):
                        errors.append(f"No data found for {sym}")
                        continue

                    stock_data = {
                        "name": info.get("longName") or info.get("shortName") or sym,
                        "symbol": info.get("symbol", sym),
                        "currency": info.get("currency", "USD"),
                        "price": info.get("currentPrice"),
                        "marketCap": info.get("marketCap"),
                        "previousClose": info.get("previousClose"),
                        "open": info.get("open"),
                        "dayHigh": info.get("dayHigh"),
                        "dayLow": info.get("dayLow"),
                        "change": None,
                        "changePercent": None
                    }

                    if stock_data["price"] and stock_data["previousClose"]:
                        stock_data["change"] = stock_data["price"] - stock_data["previousClose"]
                        stock_data["changePercent"] = (stock_data["change"] / stock_data["previousClose"]) * 100

                currency = stock_data["currency"]
                conversion_rate = None

                if currency == "INR":
                    conversion_rate = 1.0
                elif currency in ["USD", "USDT", "BUSD"]:
                    if usd_inr_rate is None:
                        usd_inr_rate = get_usd_inr_rate()
                    conversion_rate = usd_inr_rate

                def to_inr(v):
                    return round(v * conversion_rate, 2) if v and conversion_rate else None

                stock_data.update({
                    "price_inr": to_inr(stock_data["price"]),
                    "previousClose_inr": to_inr(stock_data["previousClose"]),
                    "open_inr": to_inr(stock_data["open"]),
                    "dayHigh_inr": to_inr(stock_data["dayHigh"]),
                    "dayLow_inr": to_inr(stock_data["dayLow"]),
                    "marketCap_inr": to_inr(stock_data["marketCap"]),
                    "change_inr": to_inr(stock_data["change"]),
                    "conversionRate": conversion_rate,
                })

                stocks.append(stock_data)
=======
    except Exception:
        pass
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    stocks = []             
    primary_stock = None     
    errors = []          

    usd_inr_rate = None   

    if request.method == "POST":
        raw = request.form.get("company", "").strip()

        if raw:
       
            symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]

            for sym in symbols:
                try:
                    ticker = yf.Ticker(sym)
                    info = ticker.info

               
                    if not info or ("longName" not in info and "shortName" not in info):
                        errors.append(f"Data not found for symbol: {sym}")
                        continue

                    price = info.get("currentPrice")
                    prev_close = info.get("previousClose")
                    open_price = info.get("open")
                    day_high = info.get("dayHigh")
                    day_low = info.get("dayLow")
                    market_cap = info.get("marketCap")
                    currency = info.get("currency", "USD")

         
                    change = None
                    change_percent = None
                    if price is not None and prev_close not in (None, 0):
                        change = price - prev_close
                        change_percent = (change / prev_close) * 100

                 
                    conversion_rate = None 

                    if currency == "INR":
                        conversion_rate = 1.0
                    elif currency == "USD":
                        if usd_inr_rate is None:
                            usd_inr_rate = get_usd_inr_rate()
                        conversion_rate = usd_inr_rate
                    else:
                     
                        conversion_rate = None

                    def to_inr(value):
                        if value is None or conversion_rate is None:
                            return None
                        return value * conversion_rate

                    price_inr = to_inr(price)
                    prev_close_inr = to_inr(prev_close)
                    open_inr = to_inr(open_price)
                    day_high_inr = to_inr(day_high)
                    day_low_inr = to_inr(day_low)
                    market_cap_inr = to_inr(market_cap)
                    change_inr = to_inr(change)

                    stock = {
                        "name": info.get("longName") or info.get("shortName") or "N/A",
                        "symbol": info.get("symbol", sym),
                        "currency": currency,
                        "price": price,
                        "price_inr": price_inr,
                        "marketCap": market_cap,
                        "marketCap_inr": market_cap_inr,
                        "previousClose": prev_close,
                        "previousClose_inr": prev_close_inr,
                        "open": open_price,
                        "open_inr": open_inr,
                        "dayHigh": day_high,
                        "dayHigh_inr": day_high_inr,
                        "dayLow": day_low,
                        "dayLow_inr": day_low_inr,
                        "change": change,
                        "change_inr": change_inr,
                        "changePercent": change_percent,
                        "conversionRate": conversion_rate,
                    }
                    stocks.append(stock)

                except Exception as e:
                    errors.append(f"Error fetching {sym}: {str(e)}")
>>>>>>> 87d35b4d686ba401422d1cc51c9c027048185338

            if stocks:
                primary_stock = stocks[0]

<<<<<<< HEAD
    chart = generate_candles(primary_stock["symbol"]) if primary_stock else None

    return render_template("index.html", stocks=stocks, primary_stock=primary_stock, errors=errors, chart=chart)
=======
    return render_template(
        "index.html",
        stocks=stocks,
        primary_stock=primary_stock,
        errors=errors,
    )
>>>>>>> 87d35b4d686ba401422d1cc51c9c027048185338

if __name__ == "__main__":
    app.run(debug=True)
