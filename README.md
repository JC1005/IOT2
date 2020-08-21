# IOT2

## How to use
## Credentials
The 'credentials' folder must contain
```
.aws/credentials	# AWS CLI credentials for dynamoDB
azure.ini		# Store Azure environment config
certificate.pem.crt     # service certificate
host.txt        	# contains your MQTT host ip or hostname
private.pem.key    	# service private key
rootca.pem     		# root CA certificate
twilio.ini		# Store Twilio SID, token, etc
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
- Azure Machine Learning studio
