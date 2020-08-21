#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-6.html
#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-7.html
# https://aws.amazon.com/premiumsupport/knowledge-center/create-gsi-dynamodb/
# https://dynobase.dev/dynamodb-python-with-boto3/


def get_data_from_dynamodb():
    try:
            import boto3
            from boto3.dynamodb.conditions import Key, Attr

            table_name = 'iotassign2'
            print(f"Querying table {table_name}")
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table(table_name)

            response = table.query(
                #KeyConditionExpression=Key('bookingid').eq('0.0'),
                # Add the name of the index you want to use in your query.
                IndexName="bookingid-datetime_value-index",
                KeyConditionExpression=Key('bookingid').eq('0.0'),
                ScanIndexForward=False,
                Limit=10
            )            

            items = response['Items']

            n=10 # limit to last 10 items
            data = items[:n]
            data_reversed = data[::-1]

            return data_reversed

    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


if __name__ == "__main__":
    get_data_from_dynamodb()
