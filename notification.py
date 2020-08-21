from twilio.rest import Client


class notify:
    def __int__(self, speed):
        self.speed = speed
        self.account_sid = "ACbccd3db34b4bff24f34b8506b66f4f18"
        self.auth_token = "bc9b7fb17ae371aaf3cfd407066ec765"
        self.client = Client(account_sid, auth_token)
        self.myhp = "+6593545987"
        self.twiliohp = "+12034635166"

    def alert(self):
        if self.speed > 50:
            sms = "Be careful, you are already going at a speed above 50KM/H!!!"
            message = client.api.account.messages.create(
                to=self.myhp, from_=self.twiliohp, body=sms
            )

