from flask import Flask, render_template, request
from project3 import fetch_stock_data, filter_data_by_date, generate_and_show_chart

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        stock_symbol = request.form['stock-symbol']
        begin_date = request.form['begin-date']
        end_date = request.form['end-date']
        chart_type = request.form['chart-type']
        time_series = request.form['time-series']
        
        data = fetch_stock_data(stock_symbol, time_series)
        timeseries_key = list(data.keys())[1]
        timeseries = data[timeseries_key]
        filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low = filter_data_by_date(timeseries, begin_date, end_date)
        chart_url = generate_and_show_chart(stock_symbol, chart_type, filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low, begin_date, end_date)
        return render_template('home.html', chart_url=chart_url)
    
    return render_template('home.html', chart_url=None)

if __name__ == '__main__':
    app.run(debug=True)
