from flask import Flask, Response
import requests
import json
import pandas as pd
from prophet import Prophet

# create our Flask app
app = Flask(__name__)

def get_coingecko_url(token):
    base_url = "https://api.coingecko.com/api/v3/coins/"
    token_map = {
        'ETH': 'ethereum',
        'SOL': 'solana',
        'BTC': 'bitcoin',
        'BNB': 'binancecoin',
        'ARB': 'arbitrum'
    }
    
    token = token.upper()
    if token in token_map:
        url = f"{base_url}{token_map[token]}/market_chart?vs_currency=usd&days=30&interval=daily"
        return url
    else:
        raise ValueError("Unsupported token")

def handle_outliers(df):
    # Removing outliers using IQR (Interquartile Range) method
    Q1 = df['y'].quantile(0.25)
    Q3 = df['y'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['y'] >= lower_bound) & (df['y'] <= upper_bound)]
    return df

# define our endpoint
@app.route("/inference/<string:token>")
def get_inference(token):
    """Generate inference for given token."""
    try:
        # Get the data from Coingecko
        url = get_coingecko_url(token)
    except ValueError as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-nAPPCZX8GJabu1x36iKq7ePq"  # Replace with your API key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["prices"])
        df.columns = ["ds", "y"]
        df["ds"] = pd.to_datetime(df["ds"], unit='ms')
        df = df[:-1]  # Removing today's price
        df = handle_outliers(df)  # Handling outliers
        print(df.tail(5))
    else:
        return Response(json.dumps({"Failed to retrieve data from the API": str(response.text)}),
                        status=response.status_code,
                        mimetype='application/json')

    # Fit the model using Prophet with custom parameters
    model = Prophet(
        seasonality_mode='multiplicative', 
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0,
        holidays_prior_scale=10.0
    )

    # Adding custom weekly seasonality
    model.add_seasonality(name='weekly', period=7, fourier_order=3)
    model.fit(df)

    # Make a forecast for the next 7 days
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    # Get the forecasted values for the next 7 days
    forecasted_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7).to_dict(orient='records')
    print(forecasted_values)  # Print the forecasted values

    return Response(json.dumps(forecasted_values), status=200, mimetype='application/json')

# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

