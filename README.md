# Installation Setup

You should buy VPS which is fulfilling all these requirements :

Full Documentatio: https://docs.allora.network/devs/workers/walkthroughs/walkthrough-hugging-face-worker

# System requirements
```
Operating System : Ubuntu 22.04
CPU: Minimum of 1/2 core.
Memory: 2 to 4 GB.
Storage: SSD or NVMe with at least 5GB of space.
```
- Clone repository 

```
cd $HOME
git clone https://github.com/0xtnpxsgt/allora-worker-new-udpate.git
cd allora-worker-new-udpate
```
- Edit config.json file

```
 nano config.json
```
- Copy & Paste Inside
- Change WalletName and Seedphrase

```
{
    "wallet": {
        "addressKeyName": "WalletName",
        "addressRestoreMnemonic": "SeedPhrase",
        "alloraHomeDir": "",
        "gas": "auto",
        "gasAdjustment": 1.2,
        "gasPrices": "10",
        "gasPriceUpdateInterval": 60,
        "maxFees": 25000000,
        "nodeRpc": "https://allora-rpc.testnet.allora.network",
        "maxRetries": 5,
        "retryDelay": 3,
        "accountSequenceRetryDelay": 5,
        "submitTx": true,
        "blockDurationEstimated": 10,
        "windowCorrectionFactor": 0.8
    },
    "worker": [
        {
            "topicId": 1,
            "inferenceEntrypointName": "apiAdapter",
            "loopSeconds": 2,
            "parameters": {
                "InferenceEndpoint": "http://inference:8000/inference/{Token}",
                "Token": "ETH"
            }
        },
        {
            "topicId": 2,
            "inferenceEntrypointName": "apiAdapter",
            "loopSeconds": 4,
            "parameters": {
                "InferenceEndpoint": "http://inference:8000/inference/{Token}",
                "Token": "ETH"
            }
        },
        {
            "topicId": 7,
            "inferenceEntrypointName": "apiAdapter",
            "loopSeconds": 6,
            "parameters": {
                "InferenceEndpoint": "http://inference:8000/inference/{Token}",
                "Token": "ETH"
            }
        }
    ]
}
```
- Export Variables

```
chmod +x init.config
./init.config 
```
- Deploy the Node

```
docker compose pull
docker compose up --build -d
```
- to check logs run command
```
docker compose logs -f worker
```
