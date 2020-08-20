from time import sleep
import sys
import json

from datetime import datetime  
from datetime import timedelta  
import argparse

from IOTAssignmentClientdorachua.GrabCarClient import GrabCarClient
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager
from IOTAssignmentUtilitiesdorachua.MySQLManager import QUERYTYPE_DELETE, QUERYTYPE_INSERT
from twilio.rest import Client

account_sid = "AC8e5e42b8da295d056c9b6ca6743fa9c0"
auth_token = "797c99c916d6c8f6fd7284bf8d205e81"
client = Client(account_sid, auth_token)

my_hp = "+6596678049"
twilio_hp = "+12057496895"

def getData(gcc,sqlm,datetime_start):    
    while True:
        try:
            reading = gcc.get_reading()            

            if reading is not None and len(reading)>0:
                readings = json.loads(reading)
                            
                for str_reading in readings:
                    r = json.loads(str_reading)
                    
                    if r["speedkmhour"] > 1000:
                        sms = "SMS sent! TOO FAST YOU ARE GOING MORE 90KM/H"
                        print(sms)
                        message = client.api.account.messages.create(to=my_hp, from_=twilio_hp, body=sms)
					
                    if sqlm.isconnected:

                        #print("Inserting data ...")
                        sql = "INSERT INTO iotapp (bookingid,bookingidwithtime,datetimestart_value,seconds,speed,speedkmhour,acceleration_x,acceleration_y,acceleration_z,datetime_value) VALUES (%(bookingid)s,%(bookingidwithtime)s,%(datetimestart_value)s,%(seconds)s,%(speed)s,%(speedkmhour)s,%(acceleration_x)s,%(acceleration_y)s,%(acceleration_z)s,%(datetime_value)s)"
                        bid = r["bookingid"]                                                
                        seconds = r["seconds"]
                        speed = r["speed"]
                        speedkmhour = r["speedkmhour"]
                        acceleration_x = r["acceleration_x"]
                        acceleration_y = r["acceleration_y"]
                        acceleration_z = r["acceleration_z"]
                        datetime_value = datetime_start + timedelta(seconds=seconds)
                        datetimestart_value = str(datetime_start)
                        bidwithtime = f"{bid}_{datetimestart_value}"
                        #print(f"bid,seconds,speed,speedkmhour,datetime_value {bid} {seconds} {speed} {speedkmhour} {datetime_value}")
                        data = {'bookingid': bid , 'bookingidwithtime':bidwithtime,'datetimestart_value':datetimestart_value,'seconds': seconds,'speed': speed,'speedkmhour': speedkmhour, 'acceleration_x': acceleration_x, 'acceleration_y': acceleration_y, 'acceleration_z': acceleration_z, 'datetime_value':datetime_value} 
                        success = mysqlm.insertupdatedelete(QUERYTYPE_INSERT,sql,data)
                        if success:
                            print(f"{data} inserted")

                    else:
                        print("Not connected to database")

                    
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
        host,port = "127.0.0.1", 8889
        parser = argparse.ArgumentParser()
        parser.add_argument('host')
        parser.add_argument('port',type=int)
        
        args = parser.parse_args()
        if args.host:
            host = args.host
        if args.port:
            port = args.port

        mygcc = GrabCarClient(host,port)

        u='iotuser';pw='iotpassword';h='localhost';db='iotdatabase'

        mysqlm =  MySQLManager(u,pw,h,db)
        mysqlm.connect()

        #print("Truncating records from database first...")
        #mysqlm.insertupdatedelete(QUERYTYPE_DELETE, "DELETE FROM iotapp",{})

        print("Streaming started")        
        datetime_start = datetime.now()
        gen = getData(mygcc,mysqlm,datetime_start)

        while True:
            next(gen)
            sleep(2)
        
    except KeyboardInterrupt:
        print('Interrupted')
        mysqlm.disconnect()
        sys.exit()


    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])       



