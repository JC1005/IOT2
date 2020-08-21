# IOT2

## How to use
## Credentials
The 'credentials' folder must contain
```
host.txt        # contains your MQTT host ip or hostname
*.crt           # service certificate
*private.key    # service private key
*rootCA.pem     # root CA certificate
```
## Running the web
Install dependencies
```
pip install -r ./requirements
```
Run the web application
```
python server.py
# or
python3 server.py
```

## Services used
- AWS EC2
- AWS DynamoDB
- AWS IoT
- AWS S3
