import pandas as pd
import requests
import json

def load_data(symbol, start_date, end_date, kline_type='day'):
    """
    Loads data from web.ifzq.gtimg.cn.

    Args:
        symbol (str): The stock symbol (e.g., 'sh000001').
        start_date (str): The start date (e.g., '2023-04-24').
        end_date (str): The end date (e.g., '2023-04-28').
        kline_type (str): The kline type (e.g., 'day', 'week', 'month').

    Returns:
        pandas.DataFrame: The loaded data.
    """
    url = 'http://web.ifzq.gtimg.cn/appstock/app/kline/kline'
    # Calculate the number of klines to retrieve
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    kline_num = (end - start).days + 1

    params = {
        '_var': 'kline_' + kline_type,
        'param': f'{symbol},{kline_type},{start_date},{end_date},{kline_num}'
    }
    headers = {
        'Referer': 'http://stockhtm.finance.qq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.text
        print(f"Raw response: {data}")  # Print the raw response

        try:
            # Find the start of the JSON data
            start_index = data.find('{')
            if start_index == -1:
                raise ValueError("No JSON data found in response")

            # Extract the JSON data
            json_string = data[start_index:]

            # Load the JSON data
            json_data = json.loads(json_string)
            print(f"JSON data: {json_data}")  # Print the parsed JSON data

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print(f"Failing JSON string: {json_string}")
            return None

        kline_data = json_data['data'][symbol]['day']
        df = pd.DataFrame(kline_data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
        df = df.set_index('Date')
        df = df.astype(float)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing data: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    symbol = 'sh000001'
    start_date = '2023-04-24'
    end_date = '2023-04-28'
    data = load_data(symbol, start_date, end_date)

    if data is not None:
        print("Data loaded successfully:")
        print(data.head())
