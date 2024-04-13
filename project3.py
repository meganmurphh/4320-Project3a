import requests
import plotly.graph_objs as go
import plotly.offline as pyo
import webbrowser
import os
import datetime
import requests
import webbrowser

def get_user_input():
    print("\x1b[6;30;45m" + "Enter the stock symbol" + "\x1b[0m")
    stock_symbol = input()

    print("\x1b[6;30;42m" + "Chart types" + "\x1b[0m")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    print("")
    chart_type = input_chart_type()

    print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    time_series_function = input_time_series_function()

    print("\x1b[6;30;45m" + "Enter the beginning date (YYYY-MM-DD)" + "\x1b[0m")
    begin_date = input_date()

    print("\x1b[6;30;45m" + "Enter the end date (YYYY-MM-DD):" + "\x1b[0m")
    end_date = input_date()

    while begin_date > end_date:
        print("The beginning date cannot be after the end date. Please try again.")
        begin_date = input_date("Enter the beginning date (YYYY-MM-DD): ")
        end_date = input_date("Enter the end date (YYYY-MM-DD): ")

    return stock_symbol, chart_type, time_series_function, begin_date, end_date

def input_chart_type():
    while True:
        print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
        chart_type = input()
        if chart_type in ["1", "2"]:
            return "bar" if chart_type == "1" else "line"
        else:
            print("Invalid chart type. Please try again.")

def input_time_series_function():
    while True:
        print("\x1b[6;30;45m" + "Enter the time series function: " + "\x1b[0m")
        time_series_function = input()
        if time_series_function in ["1", "2", "3", "4"]:
            if time_series_function == "1":
                return "TIME_SERIES_INTRADAY"
            elif time_series_function == "2":
                return "TIME_SERIES_DAILY"
            elif time_series_function == "3":
                return "TIME_SERIES_WEEKLY"
            else:
                return "TIME_SERIES_MONTHLY"
        else:
            print("Invalid time series function. Please try again.")

def input_date(prompt=""):
    while True:
        date = input(prompt)
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect date format, should be YYYY-MM-DD")

def fetch_stock_data(stock_symbol, time_series_function):
    url = f"https://www.alphavantage.co/query?function={time_series_function}&symbol={stock_symbol}&interval=5min&apikey=TKD85DJRC6KNT94C"
    r = requests.get(url)
    data = r.json()
    if 'Error Message' in data:
        print("API Error:", data['Error Message'])
        return None
    return data


def filter_data_by_date(timeseries, begin_date, end_date):
    filtered_dates = []
    filtered_values_close = []
    filtered_values_open = []
    filtered_values_high = []
    filtered_values_low = []
    for date, value in timeseries.items():
        if begin_date <= date <= end_date:
            filtered_dates.append(date)
            filtered_values_close.append(float(value['4. close']))
            filtered_values_open.append(float(value['1. open']))
            filtered_values_high.append(float(value['2. high']))
            filtered_values_low.append(float(value['3. low']))
    return filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low


def generate_and_show_chart(stock_symbol, chart_type, filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low, begin_date, end_date):
    if chart_type == 'line':
        trace_close = go.Scatter(x=filtered_dates, y=filtered_values_close, mode='lines', name='Close')
        trace_open = go.Scatter(x=filtered_dates, y=filtered_values_open, mode='lines', name='Open')
        trace_high = go.Scatter(x=filtered_dates, y=filtered_values_high, mode='lines', name='High')
        trace_low = go.Scatter(x=filtered_dates, y=filtered_values_low, mode='lines', name='Low')
    else:
        trace_close = go.Bar(x=filtered_dates, y=filtered_values_close, name='Close')
        trace_open = go.Bar(x=filtered_dates, y=filtered_values_open, name='Open')
        trace_high = go.Bar(x=filtered_dates, y=filtered_values_high, name='High')
        trace_low = go.Bar(x=filtered_dates, y=filtered_values_low, name='Low')

    data = [trace_close, trace_open, trace_high, trace_low]
    layout = go.Layout(title=f'Stock Prices for {stock_symbol} from {begin_date} to {end_date}')
    fig = go.Figure(data=data, layout=layout)

    file_name = 'stock_chart.html'
    file_path = os.path.join(os.getcwd(), file_name)
    pyo.plot(fig, filename=file_path, auto_open=False)

    if not webbrowser.open('file://' + file_path):
        try:
            webbrowser.open_new('file://' + file_path)
        except:
            try:
                webbrowser.open_new_tab('file://' + file_path)
            except Exception as e:
                print(f"Failed to open the browser: {e}")


def main():
    stock_symbol, chart_type, time_series_function, begin_date, end_date = get_user_input()
    data = fetch_stock_data(stock_symbol, time_series_function)
    
    if not data:
        print("Error: Empty data returned from the API.")
        return
    
    timeseries_key = list(data.keys())[1]  # Assuming the timeseries data is at index 1
    timeseries = data[timeseries_key]
    filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low = filter_data_by_date(timeseries, begin_date, end_date)
    generate_and_show_chart(stock_symbol, chart_type, filtered_dates, filtered_values_close, filtered_values_open, filtered_values_high, filtered_values_low, begin_date, end_date)




if __name__ == "__main__":
    main()