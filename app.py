from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

#tickers = pd.read_csv('https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/WIKI_tickers.csv')
tickers = pd.read_csv('tickers.csv')

ticker_symbols = tickers['quandl code'].values


#@app.route('/')
#def main():
#  return redirect('/index')

#@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    print("request.method:", request.method)
    print("request.form:", request.form)
    if request.method == 'POST' and 'symbol' in request.form:
        sym = request.form['symbol'].upper()
        print('sym: ', sym)
        #print('sym.upper: ', sym)
        #if 'WIKI/' + sym.upper() in ticker_symbols:
        if 'WIKI/' + sym in ticker_symbols:
            try:
                return render_template('index.html', place_holder="I know that symbol")
            except:
                return render_template('index.html', place_holder="Fail.")
        else:
            return render_template('index.html', place_holder="I do not know this symbol")
    else:
        print("first else...")
        return render_template('index.html', place_holder="Please input a stock symbol...")

#@app.route('/404')
#def not_found():
#    return render_template('404.html')


if __name__ == '__main__':
    app.run(port=33507)
