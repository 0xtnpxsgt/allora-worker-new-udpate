# Allora-worker-new-udpate
Allora Worker Chronos Model

- You must need to buy a VPS for running Allora Worker
- You can buy from : Contabo
- You should buy VPS which is fulfilling all these requirements : 
```bash
Operating System : Ubuntu 22.04
CPU: Minimum of 1/2 core.
Memory: 2 to 4 GB.
Storage: SSD or NVMe with at least 5GB of space.
```
# Prerequisites
Before you start, ensure you have docker compose installed.

### Deployment - Read Carefully! 
## Step 1: 
```bash
git clone https://github.com/allora-network/basic-coin-prediction-node
```
## Step 2: 
```bash
cd basic-coin-prediction-node
```
## Step 3: Copy and Populate Configuration 
```bash
cp config.example.json config.json
```
## Step 4: 
Edit addressKeyName & addressRestoreMnemonic & Copy / Paste inside config.json
```bash
sudo rm -rf config.json && sudo nano config.json
```
See example here:
```
{
    "wallet": {
        "addressKeyName": "YOUR_WALLET_NAME",
        "addressRestoreMnemonic": "SEED_PHASE",
        "alloraHomeDir": "",
        "gas": "1000000",
        "gasAdjustment": 1.0,
        "nodeRpc": "https://sentries-rpc.testnet-1.testnet.allora.network",
        "maxRetries": 1,
        "delay": 1,
        "submitTx": false
    },
    "worker": [
        {
            "topicId": 1,
            "inferenceEntrypointName": "api-worker-reputer",
            "loopSeconds": 5,
            "parameters": {
                "InferenceEndpoint": "http://inference:8000/inference/{Token}",
                "Token": "ETH"
            }
 },
    {
      "topicId": 2,
      "inferenceEntrypointName": "api-worker-reputer",
      "loopSeconds": 5,
      "parameters": {
        "InferenceEndpoint": "http://localhost:8000/inference/{Token}",
        "Token": "ETH"
      }
    }
  ]
}

```

## Step 5: Edit App.py
- Register on Coingecko https://www.coingecko.com/en/developers/dashboard & Create Demo API KEY
- Copy & Replace API with your `COINGECKO API` , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf app.py && sudo nano app.py
```
```bash
from flask import Flask, Response
import requests
import json
import pandas as pd
import torch
from chronos import ChronosPipeline
 
# create our Flask app
app = Flask(__name__)
 
# define the Hugging Face model we will use
model_name = "amazon/chronos-t5-tiny"
 
# define our endpoint
@app.route("/inference/<string:token>")
def get_inference(token):
    """Generate inference for given token."""
    if not token or token != "ETH":
        error_msg = "Token is required" if not token else "Token not supported"
        return Response(json.dumps({"error": error_msg}), status=400, mimetype='application/json')
    try:
        # use a pipeline as a high-level helper
        pipeline = ChronosPipeline.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    except Exception as e:
        return Response(json.dumps({"pipeline error": str(e)}), status=500, mimetype='application/json')
 
    # get the data from Coingecko
    # here we'll use last 30 days of ETH/USD
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=30&interval=daily"
 
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-XXXXXXXXXXXXXXXXXXX" # replace with your API key
    }
 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["prices"])
        df.columns = ["date", "price"]
        df["date"] = pd.to_datetime(df["date"], unit = "ms")
        df = df[:-1] # removing today's price
        print(df.tail(5))
    else:
        return Response(json.dumps({"Failed to retrieve data from the API": str(response.text)}), 
                        status=response.status_code, 
                        mimetype='application/json')
 
    # define the context and the prediction length
    context = torch.tensor(df["price"])
    prediction_length = 1
 
    try:
        forecast = pipeline.predict(context, prediction_length)  # shape [num_series, num_samples, prediction_length]
        print(forecast[0].mean().item()) # taking the mean of the forecasted prediction
        return Response(str(forecast[0].mean().item()), status=200)
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
 
# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
```

## Step 6: Create main.py file
- Copy & Paste this code: , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf main.py && sudo nano main.py
```
```bash
import requests
import sys
import json
 
def process(argument):
    headers = {'Content-Type': 'application/json'}
    url = f"http://inference:8000/inference/{argument}"
    response = requests.get(url, headers=headers)
    return response.text
 
if __name__ == "__main__":
    # Your code logic with the parsed argument goes here
    try:
        if len(sys.argv) < 5:
            value = json.dumps({"error": f"Not enough arguments provided: {len(sys.argv)}, expected 4 arguments: topic_id, blockHeight, blockHeightEval, default_arg"})
        else:
            topic_id = sys.argv[1]
            blockHeight = sys.argv[2]
            blockHeightEval = sys.argv[3]
            default_arg = sys.argv[4]
            
            response_inference = process(argument=default_arg)
            response_dict = {"infererValue": response_inference}
            value = json.dumps(response_dict)
    except Exception as e:
        value = json.dumps({"error": {str(e)}})
    print(value)
```
## Step 7: Create requirments.txt
- Copy & Paste this code: , then save `Ctrl+X Y ENTER`.
```bash
sudo rm -rf requirements.txt && sudo nano requirements.txt
```
```bash
flask[async]
gunicorn[gthread]
transformers[torch]
pandas
git+https://github.com/amazon-science/chronos-forecasting.git
```
## Step 8: Export Variables
```bash
chmod +x init.config
./init.config
```
## Step 9: Docker Build - This will take time

```bash
docker compose up --build
```

if the logs shows like this, then your allora worker is running successfully. 

<img width="1535" alt="Screenshot 1403-05-23 at 7 21 56 PM" src="https://github.com/user-attachments/assets/602d31d0-48b4-4666-bf55-feaa3d2ab3ff">

## Testing
```bash
curl http://localhost:8000/inference/<token>
```

Congrats!







