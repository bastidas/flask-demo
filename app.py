from flask import Flask, render_template, request, redirect, Markup
import pandas as pd
import flask

app = Flask(__name__)

tickers = pd.read_csv('https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/WIKI_tickers.csv')
#tickers = pd.read_csv('tickers.csv')

ticker_symbols = tickers['quandl code'].values



from bokeh.plotting import figure
#from bokeh.resources import CDN
from bokeh.embed import components
#from bokeh.models import NumeralTickFormatter
import numpy as np
import datetime

#from bokeh.embed import components
#from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8



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
    #script, div = components(plot)#, CDN)


    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(plot)


    print('returned')
    return script, div, js_resources, css_resources
    #return Markup(script), Markup(div)


def simple_plot(symbl, name):
    x = list(range(0, 10 + 1))
    fig = figure(title=name)
    fig.line(x, [i ** 2 for i in x], line_width=2)
    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(fig)
    return script, div, js, css



#@app.route('/')
#def main():
#  return redirect('/index')

#@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
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
                #x = list(range(0, 100 + 1))
                #print(x)
                #fig = figure(title=stock)
                #print('fig1')
                #fig.line(x, [i ** 2 for i in x], line_width=2)
                #print('fig2')
                #js_resources = INLINE.render_js()
                #c = INLINE.render_css()
                #print('js cs reccoures')
                #script, div = components(fig)
                #print('made fig')
                script, div, js, css = simple_plot(sym, stock)
                html = flask.render_template('index.html', place_holder="Enter a stock symbol", plot_script=script, plot_div=div, js_resources=js, css_resources=css)
                print('returning html')
                #return render_template('index.html', place_holder="I know that symbol", 
                #  plot_script=posted_script, plot_div=posted_div)
                return encode_utf8(html)
                #return html
            except:
                #return render_template('index.html', place_holder="Fail.")
                html = flask.render_template('index.html', place_holder="Fail. Something went wrong", js_resources=js_resources, css_resources=css_resources)  
                return html
        else:
            #return render_template('index.html', place_holder="I do not know this symbol")
            html = flask.render_template('index.html', place_holder="Invalid symbol", js_resources=js_resources, css_resources=css_resources)  
            return html
    else:
        #js_resources = INLINE.render_js()
        #css_resources = INLINE.render_css()
        html = flask.render_template('index.html', place_holder="Enter a stock symbol", js_resources=js_resources, css_resources=css_resources)  
        return html

#@app.route('/404')
#def not_found():
#    return render_template('404.html')


if __name__ == '__main__':
    app.run(port=33507)
