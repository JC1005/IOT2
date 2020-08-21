from azureml.core.workspace import Workspace
import requests
import configparser
import json
from aws import awsBoto3
from boto3.dynamodb.conditions import Key, Attr
import numpy as np
import joblib


class machineLearning:
    def __init__(self):
        configFilePath = "credentials/azure.ini"
        self.azureConfig = configparser.ConfigParser()
        try:
            self.azureConfig.read(configFilePath)
            self.ws = Workspace(
                subscription_id=self.azureConfig["default"]["subscription_id"],
                resource_group=self.azureConfig["default"]["resource_group"],
                workspace_name=self.azureConfig["default"]["workspace_name"],
            )
        except:
            print("Azure config file not found at " + configFilePath)
            print("A template will be provided.")
            self.azureConfig["default"] = {
                "subscription_id": "paste your subscription ID here",
                "resource_group": "paste your resource group here",
                "workspace_name": "paste your workspace name here",
                "scoring_uri": "paste your scoring uri here",
            }
            with open(configFilePath, "w") as configfile:
                self.azureConfig.write(configfile)

    def predict(self, raw_data):
        headers = {"Content-Type": "application/json"}
        # dataJSON = json.dumps(data)
        # dataBytes = bytes(dataJSON, encoding="utf8")
        resp = requests.post(
            "http://3e48b02b-9d9c-417d-95c0-e99482e30802.eastus.azurecontainer.io/score",
            raw_data,
            headers=headers,
        )
        return resp.text


if __name__ == "__main__":
    ml = machineLearning()
    table_name = "iotassign2"
    index_name = "bookingid-datetime_value-index"
    awsBoto = awsBoto3()
    dynamodb = awsBoto.session.resource("dynamodb", "us-east-1")
    table = dynamodb.Table(table_name)
    response = table.query(
        # KeyConditionExpression=Key('bookingid').eq('0.0'),
        # Add the name of the index you want to use in your query.
        IndexName=index_name,
        KeyConditionExpression=Key("bookingid").eq("0.0"),
        ScanIndexForward=False,
        Limit=1,
    )

    items = response["Items"]
    print(items)
    # ml.predict(items)
