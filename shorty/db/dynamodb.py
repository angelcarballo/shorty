import boto3

class DynamoDB(object):
    def __init__(self):
        self.client = boto3.client("dynamodb",
                                   region_name="eu-west-2",
                                   endpoint_url="http://localhost:8000"
                                   )
        self.__create_urls_table()
        self.__create_users_table()

    def has_user(self, email):
        raise NotImplemented()

    def get_user(self, email):
        raise NotImplemented()

    def store_user(self, user):
        raise NotImplemented()

    def has_key(self, key):
        raise NotImplemented()

    def get_url(self, key):
        raise NotImplemented()

    def store_url(self, key, url):
        raise NotImplemented()

    def __create_urls_table(self):
        existing_tables = self.client.list_tables()["TableNames"]
        if "urls" not in existing_tables:
            table = self.client.create_table(
                TableName="urls",
                KeySchema=[
                    {"AttributeName": "key", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "key", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            self.client.get_waiter("table_exists").wait(TableName="urls")

    def __create_users_table(self):
        existing_tables = self.client.list_tables()["TableNames"]
        if "users" not in existing_tables:
            table = self.client.create_table(
                TableName="users",
                KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "email", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            self.client.get_waiter("table_exists").wait(TableName="users")
