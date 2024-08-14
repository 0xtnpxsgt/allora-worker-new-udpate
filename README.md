# Allora-3-Workers-New-Udpate 
(Topic used: ETH Topic 1 - 2 - 7)

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
```bash
# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
docker version

# Install Docker-Compose
VER=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)

curl -L "https://github.com/docker/compose/releases/download/"$VER"/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Docker Permission to user
sudo groupadd docker
sudo usermod -aG docker $USER
```
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
```bash
{
  "wallet": {
    "addressKeyName": "YOUR_WALLET_NAME",
    "addressRestoreMnemonic": "SEED_PHASE",
    "alloraHomeDir": "",
    "gas": "1000000",
    "gasAdjustment": 1.0,
    "nodeRpc": "https://sentries-rpc.testnet-1.testnet.allora.network/",
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
        "InferenceEndpoint": "http://localhost:8000/inference/{Token}",
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
    },
    {
      "topicId": 7,
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

## Step 5: Export Variables
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







