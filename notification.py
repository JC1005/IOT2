from twilio.rest import Client
import configparser
from pathlib import Path


class twilio:
    def __init__(self):
        config = configparser.ConfigParser()
        configFilePath = "credentials/twilio.ini"
        # check if config file is exists
        # if exist, read and store credentials in variables
        if Path(configFilePath).exists():
            try:
                config.read(configFilePath)
                account_sid = config["default"]["account_sid"]
                auth_token = config["default"]["auth_token"]
                self.twiliohp = config["default"]["twiliohp"]
                self.client = Client(account_sid, auth_token)
            except:
                print(configFilePath + "is corrupted")
        # if config file don't exist, provide a template at configFilePath
        else:
            print(configFilePath + "not found, a template will be provided.")
            config["default"] = {
                "account_sid": "paste your account SID here",
                "auth_token": "paste your authentication token here",
                "twiliohp": "paste your twilio provided number here",
            }
            with open(configFilePath, "w") as configfile:
                config.write(configfile)

    def alert(self, speed, dest_hp):
        if speed > 50:
            sms = "Be careful, you are already going at a speed above 50KM/H!!!"
            message = self.client.api.account.messages.create(
                to=dest_hp, from_=self.twiliohp, body=sms
            )
            return message


if __name__ == "__main__":
    twilio = twilio()
    print(twilio.alert(80, "81234567"))
