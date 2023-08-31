# Here lies class for working with native GraphQL API

import requests


class NativeRbData:
    def __init__(self, email:str, password:str,api_url="https://api.rbdata.ru/graphql"):
        self.api_url=api_url
        if email is None or password is None:
            raise AttributeError("NativeRbData: email and password should not be none")
        self.__email=email
        self.__password=password

        
    def get_token(self)->str:
        graphql_query="""
            mutation {{
                session {{
                    createWithPassword(
                            input:{{
                                email:"{email}",
                                password:"{password}"}})
                        {{
                        sessionTokens{{
                            accessToken
                        }}
                    }}
                }}
            }}
            """.format(email=self.__email,password=self.__password)
 
        request_body={"query":graphql_query}
        resp=requests.post(self.api_url,json=request_body)
        if not resp.ok:
            print("Cant get token from graphql")
            return None
        
        try:
            token=resp.json()['data']['session']['createWithPassword']['sessionTokens']['accessToken']
            return token
        except Exception:
            print("cant parse answer from graphql, when trying to get token")
            return None

