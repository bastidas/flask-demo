from flask import Flask, render_template, request, redirect, Markup
import pandas as pd

app = Flask(__name__)

tickers = pd.read_csv('https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/WIKI_tickers.csv')
#tickers = pd.read_csv('tickers.csv')

ticker_symbols = tickers['quandl code'].values



from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
#from bokeh.models import NumeralTickFormatter
import numpy as np
import datetime

def generate_plot(symbl, name):
    print("inside generate plot")
    end_date = datetime.datetime.now()
    print("end_date: ", end_date)
    start_date = end_date + datetime.timedelta(-30)
    print("start_date: ", start_date)
    print("name:", name)
    x = np.arange(0,100,10) 
    y = .2 * x * x - 3 #np.range(0,100,1)*2.0
    print("x:", x)
    print("y:", y)
    plot = figure(title=name, tools='wheel_zoom, pan',
                  responsive=True, plot_width=850,
                  plot_height=500)#, x_axis_type='datetime')
    #x = np.range(0,100,10) 
    #y = 2 * x * x + 3 #np.range(0,100,1)*2.0
    print("figured")
    plot.line(x,y)
    print("plotted")

    #print("creating plot")
    #plot = figure(title=name, tools='wheel_zoom, pan',
    #              responsive=True, plot_width=1000,
    #              plot_height=500, x_axis_type='datetime')
    #df = get_data(symbl)
    #plot.line(df['date'], df['close'], legend='Closing Price')
    #plot.legend.orientation = 'top_left'
    #plot.legend.background_fill_alpha = 0.5
    #plot.yaxis[0].formatter = NumeralTickFormatter(format='$0.00')
    script, div = components(plot, CDN)
    print('returned')
    return Markup(script), Markup(div)



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
        #print('sym: ', sym)
        #print('sym.upper: ', sym)
        #if 'WIKI/' + sym.upper() in ticker_symbols :
        if 'WIKI/' + sym in ticker_symbols:
            print('matched')
            try:
                print('getting stock')
                stock = tickers.loc[tickers['quandl code'] == 'WIKI/' + sym, 'name'].values[0]
                print('generating plot')
                print('sym: ', sym)
                print('stock:', stock)
                posted_script, posted_div = generate_plot(sym, stock)
                print("rendering_template")
                return render_template('index.html', place_holder="I know that symbol", 
                  plot_script=posted_script, plot_div=posted_div)
            except:
                return render_template('index.html', place_holder="Fail.")
        else:
            return render_template('index.html', place_holder="I do not know this symbol")
    else:
        #print("first else...")
        return render_template('index.html', place_holder="Please input a stock symbol...")

#@app.route('/404')
#def not_found():
#    return render_template('404.html')


if __name__ == '__main__':
    app.run(port=33507)
