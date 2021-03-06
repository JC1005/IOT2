from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
from pathlib import Path
import boto3
import configparser
from boto3.dynamodb.conditions import Key, Attr


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


class awsMQTT:
    def __init__(self):
        with open("credentials/host.txt", "r") as f:
            self.host = f.read()
        self.rootCAPath = "credentials/rootca.pem"
        self.certificatePath = "credentials/certificate.pem.crt"
        self.privateKeyPath = "credentials/private.pem.key"

        self.MQTTClient = AWSIoTMQTTClient("uniquePlaceholder")
        self.MQTTClient.configureEndpoint(self.host, 8883)
        self.MQTTClient.configureCredentials(
            self.rootCAPath, self.privateKeyPath, self.certificatePath
        )
        self.MQTTClient.configureOfflinePublishQueueing(
            -1
        )  # Infinite offline Publish queueing
        self.MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        try:
            self.MQTTClient.connect()
        except FileNotFoundError as e:
            print(e)
        except:
            print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])

    def publish(self, topic, payload, QoS):
        self.MQTTClient.publish(topic, payload, QoS)

    def subscribe(self, topic, QoS):
        self.MQTTClient.subscribe(topic, QoS, customCallback)


class awsBoto3:
    def __init__(self):

        # initialize credentials and connection
        if Path("~/.aws/credentials").exists() is False:
            credentialFilePath = "credentials/.aws/credentials"
            self.AWSconfig = configparser.ConfigParser()
            try:
                self.AWSconfig.read(credentialFilePath)
            except:
                print("AWS credentials file not found at" + credentialFilePath)

            self.session = boto3.Session(
                aws_access_key_id=self.AWSconfig["default"]["aws_access_key_id"],
                aws_secret_access_key=self.AWSconfig["default"][
                    "aws_secret_access_key"
                ],
                aws_session_token=self.AWSconfig["default"]["aws_session_token"],
            )
        else:
            pass


if __name__ == "__main__":
    # awsMQTT = awsMQTT()
    awsBoto3 = awsBoto3()
    print(awsBoto3.AWSconfig["default"]["aws_access_key_id"])
    print(awsBoto3.AWSconfig["default"]["aws_secret_access_key"])
    print(awsBoto3.AWSconfig["default"]["aws_session_token"])
    table_name = "iotassign2"
    index_name = "bookingid-datetime_value-index"

    dynamodb = awsBoto3.session.resource("dynamodb", "us-east-1")
    table = dynamodb.Table(table_name)
    response = table.query(
        # KeyConditionExpression=Key('bookingid').eq('0.0'),
        # Add the name of the index you want to use in your query.
        IndexName=index_name,
        KeyConditionExpression=Key("bookingid").eq("0.0"),
        ScanIndexForward=False,
        Limit=10,
    )

    items = response["Items"]
    n = 10  # limit to last 10 items
    data = items[:n]
    data_reversed = data[::-1]
    print(data_reversed)
