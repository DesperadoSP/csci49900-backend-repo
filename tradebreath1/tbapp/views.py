from django.http import HttpResponse
from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import TimeFrame
import alpaca_trade_api as tradeapi
import datetime
import requests

# os.environ['APCA_API_KEY_ID'] = 'PK87MNNJ3DIDGDHWMTH6'
# os.environ['APCA_API_SECRET_KEY'] = 'r8llTDlXflevWpchpjkqGPHLA5QYxIRs7tfCUY6n'

api = tradeapi.REST(key_id='PK87MNNJ3DIDGDHWMTH6', secret_key='r8llTDlXflevWpchpjkqGPHLA5QYxIRs7tfCUY6n', base_url="https://paper-api.alpaca.markets")
#print(dir(TimeFrame))
#api.get_bars("AAPL", TimeFrame.Minute, "2021-06-08", "2021-06-08", adjustment='raw').df

AVAILABLE_INTERVALS = {'Day': TimeFrame.Day,
                       'Hour': TimeFrame.Hour,
                       'Minute': TimeFrame.Minute,
                       'Sec': TimeFrame.Sec}


# THIS ACTUALLY CALLS ALPACA.
# THIS ACTUALLY CALLS ALPACA.
def get_alpaca_info(stock, interval, start, end):
  if interval not in AVAILABLE_INTERVALS:
    raise Exception("Interval not supported.")

  response = requests.get("https://stocknewsapi.com/api/v1?tickers=" + stock + "&items=25&token=c5nrxp6lw6ftwokpjx08wkycksgzcg0rpgc4hlcy")
  news = (response.json())

  return api.get_bars(stock, AVAILABLE_INTERVALS[interval], start, end), news

#my_get_bar("AAPL", 'Day', "2021-06-08", "2021-06-10")

# THIS PARSES THE QUERY PARAMS FROM THE CLIENT.
# Optional end_date, inject yesterday if not provided.
def parse_query_params(stock, interval, start_date, end_date= None):
  if not (start_date and stock and interval):
    raise Exception("Missing query params.")

  if end_date is None:
    end_date = str(datetime.date.today() - datetime.timedelta(days=2))

  return {"stock": stock[0], "interval": interval[0], "start_date": start_date[0], "end_date": end_date}

# THIS IS FIRST FUNCTION CALLED.
def view_bars(request):
  parsed_params = parse_query_params(**request.GET)

  return HttpResponse(get_alpaca_info(parsed_params['stock'], parsed_params['interval'], parsed_params['start_date'], parsed_params['end_date']))

#view_bars({"stock" : "AAPL", "interval": 'Day', "start_date": "2021-06-08"})
