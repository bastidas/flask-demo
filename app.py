from flask import Flask, render_template, request, redirect, Markup
import pandas as pd
import flask
import requests

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


from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import RangeSlider
#from bokeh.layouts import column

from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

#from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.models import Select


#measures = {
#    'Value': '0',
#    'Percent':   '1',
#}


def getitem(obj, item, default):
  #'symbol' in request.form:
  #      sym = request.form['symbol'].upper()
#
    print('obj', 'obj')
    if item not in obj:
        print('not in')
        return default
    else:
        print('was in')
        return obj[item]


#x = [x*0.005 for x in range(0, 200)]
#y = x
#source = ColumnDataSource(data=dict(x=x, y=y))

#callback = CustomJS(args=dict(source=source), code="""
#    var f = cb_obj.value
#    print(f)
#    source.trigger('change');
#""")


def generate_plot(symbl, name, data_series):
 
    print("inside generate plot")
    end_date = datetime.datetime.now()
    print("end_date: ", end_date)
    start_date = end_date + datetime.timedelta(-30)
    print("start_date: ", start_date)
    api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?api_key=t-drH_WSpLdRenh1o86E&start_date=%s&end_date=%s' \
        % (symbl, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=2))
    raw_json = session.get(api_url).json()['dataset']

    #options: 
    #open/close/adjusted open/adjusted close
    #date range
    #abs or percent
    
    print('oldest_available_date: ',raw_json['oldest_available_date'])
    print('newest_available_date: ',raw_json['newest_available_date'])
    print('column_names: ', raw_json['column_names'])# ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
    df = pd.DataFrame({'date': [x[0] for x in raw_json['data']], 'close': np.array([x[4] for x in raw_json['data']]),})
    df['date'] = pd.to_datetime(df['date'])
    plot = figure(title=name, tools='wheel_zoom, box_zoom, save, reset',
                  responsive=True, plot_width=750, plot_height=400, x_axis_type='datetime')
    plot.toolbar.logo = None
    
    if data_series[0] == '1':
        opening_price = np.array([x[1] for x in raw_json['data']])
        plot.line(df['date'], opening_price, line_width=2, color="blue", legend='Opening price')

    if data_series[1] == '1':
        closing_price = np.array([x[4] for x in raw_json['data']])
        plot.line(df['date'], closing_price, line_width=2, color="green", legend='Closing price')

    if data_series[2] == '1':
        opening_adj_price = np.array([x[8] for x in raw_json['data']])
        plot.line(df['date'], opening_adj_price, line_width=2, color="grey", legend='Adjusted ppening price')

    if data_series[3] == '1':
        closing_adj_price = np.array([x[11] for x in raw_json['data']])
        plot.line(df['date'], closing_adj_price, line_width=2, color="black", legend='Adjusted closing price')

    #plot.line(df['date'], df['close'], line_width=2, legend='Closing Price')
    plot.legend.location = 'top_left'
    #plot.legend.background_fill_alpha = 0.1
    #print('trying layout?')
    #layout = column(option_button_group, date_range_slider, plot)
    #plot.yaxis[0].formatter = NumeralTickFormatter(format='$0.00')
    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(plot)
    #print('making comppnotses')
    #script, div = components(layout)
    return script, div, js, css



def get_data(symbl, name):
      x = list(range(0, 10 + 1))
      y = [i ** 2 for i in x]
      z = [-1 + .5*i ** 2 for i in x]
      return x, y, z


def create_plot(symbl, stock, data_series):
    x, y, z = get_data(symbl, stock)
    fig = figure(title=stock)
    if 'Percent' in request.form['Measure']:            
        fig.line(x, y, line_width=2, color='green')
    if 'Value' in request.form['Measure']:
        fig.line(x, z, line_width=2, color='blue')
    if data_series[0] == '1':
        fig.line(x, [1+ + .1*i ** 2 for i in x], line_width=2, color='black')
    if data_series[1] == '1':
        fig.line(x, [-1 + .5*i ** 2 for i in x], line_width=2, color='black')


    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(fig)
    return script, div, js, css


@app.route('/', methods=['GET', 'POST'])
def index():
    args = flask.request.args
    measure = getitem(request.form, 'Measure', 'Value')
    plt_open = getitem(request.form, 'open', "0")
    plt_close = getitem(request.form, 'close', "0")
    plt_adj_open = getitem(request.form, 'adj_open', "0")
    plt_adj_close = getitem(request.form, 'adj_close', "0")


    #print("sadsssdgads", plt_open, plt_close, plt_adj_open, plt_adj_close)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    print("request.from", request.form)
    if request.method == 'POST' and 'symbol' in request.form:
        sym = request.form['symbol'].upper()
        if 'WIKI/' + sym in ticker_symbols:
            try:
                stock = tickers.loc[tickers['quandl code'] == 'WIKI/' + sym, 'name'].values[0]

                #script, div, js, css = create_plot(sym,stock,[plt_open, plt_close, plt_adj_open, plt_adj_close])
                script, div, js, css = generate_plot(sym,stock,[plt_open, plt_close, plt_adj_open, plt_adj_close])

                html = flask.render_template('index.html', place_holder="Enter a stock symbol", 
                  plot_script=script, plot_div=div, js_resources=js, css_resources=css, 
                   measure = measure, open = plt_open, close = plt_close, adj_open = plt_adj_open, adj_close = plt_adj_close)
                return encode_utf8(html)
            except:
                html = flask.render_template('index.html', place_holder="Fail. Something went wrong",
                  js_resources=js_resources, css_resources=css_resources, 
                  open = plt_open, close = plt_close, adj_open = plt_adj_open, adj_close = plt_adj_close)
                return html
        else:
            html = flask.render_template('index.html', place_holder="Invalid symbol",
             js_resources=js_resources, css_resources=css_resources,
               measure = measure, open = plt_open, close = plt_close, adj_open = plt_adj_open, adj_close = plt_adj_close)  
            return html
    else:
        html = flask.render_template('index.html', place_holder="Enter a stock symbol", 
          js_resources=js_resources, css_resources=css_resources, 
           measure = measure, open = plt_open, close = plt_close, adj_open = plt_adj_open, adj_close = plt_adj_close)
        return html



if __name__ == '__main__':
    app.run(port=33507)















