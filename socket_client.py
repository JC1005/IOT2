from time import sleep
import sys
import json
from aws import awsMQTT
from datetime import datetime
from datetime import timedelta
import argparse

from IOTAssignmentClientdorachua.GrabCarClient import GrabCarClient
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import (
    QUERYTYPE_DELETE,
    QUERYTYPE_INSERT,
)

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json


def getData(gcc, datetime_start, my_rpi):
    while True:
        try:
            reading = gcc.get_reading()

            if reading is not None and len(reading) > 0:
                readings = json.loads(reading)

                for str_reading in readings:
                    r = json.loads(str_reading)
                    import uuid

                    uuid = uuid.uuid1()
                    from datetime import datetime

                    now = datetime.now()  # current date and time
                    datetime_value = now.strftime("%Y-%m-%d %H:%M:%S")
                    r["id"] = str(uuid)
                    r["datetime_value"] = datetime_value
                    print(r)
                    my_rpi.publish("sensors/speed", json.dumps(r), 1)

            yield

        except GeneratorExit:
            print("Generator Exit error")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            return

        except KeyboardInterrupt:
            exit(0)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])


if __name__ == "__main__":

    try:
        host, port = "127.0.0.1", 8889
        parser = argparse.ArgumentParser()
        parser.add_argument("host")
        parser.add_argument("port", type=int)

        args = parser.parse_args()
        if args.host:
            host = args.host
        if args.port:
            port = args.port

        mygcc = GrabCarClient(host, port)
        aws = awsMQTT()

        # Connect and subscribe to AWS IoT
        # my_rpi.connect()

        print("Streaming started")
        datetime_start = datetime.now()

        gen = getData(mygcc, datetime_start, aws.MQTTClient)

        while True:
            next(gen)
            sleep(2)

    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit()

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

