# Here lies class for working with native GraphQL API

import requests


class NativeRbData:
    def __init__(self, email:str, password:str,api_url="https://api.rbdata.ru/graphql"):
        self.api_url=api_url
        if email is None or password is None:
            raise AttributeError("NativeRbData: email and password should not be none")
        self.__email=email
        self.__password=password


