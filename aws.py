from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


class aws:
    def __init__(self):
        with open("credentials/host.txt", "r") as f:
            self.host = f.read()
        self.rootCAPath = "credentials/AmazonRootCA1.pem"
        self.certificatePath = "credentials/fa825f2405-certificate.pem.crt"
        self.privateKeyPath = "credentials/fa825f2405-private.pem.key"

        self.awsMQTT = AWSIoTMQTTClient("uniquePlaceholder")
        self.awsMQTT.configureEndpoint(self.host, 3)
        self.awsMQTT.configureCredentials(
            self.rootCAPath, self.privateKeyPath, self.certificatePath
        )

        try:
            self.awsMQTT.connect()
        except FileNotFoundError as e:
            print(e)
        except:
            print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])

    def publish(self, topic, payload, QoS):
        self.awsMQTT.publish(topic, payload, QoS)

    def subscribe(self, topic, QoS):
        self.awsMQTT.subscribe(topic, QoS, customCallback)


if __name__ == "__main__":
    aws = aws()

