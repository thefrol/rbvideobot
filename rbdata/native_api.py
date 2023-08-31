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
                                password:"{password}"
                                }})
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

    def upload_video_from_url(self, video_url, filename="Untitled video from api",organizarion_id=None):
        token=self.get_token()
        if token is None:
            raise ValueError("Cant authorize in graphql to get videos")


        graphql_query="""
            mutation{{
                video{{
                    createFromUrl(
                        input:{{
                            url:"{video_url}"
                            {organization_string}
                            filename:"{filename}"
                    }})
                    {{
                        video {{
                            id
                            name        
                        }}
                        
                        error {{
                            code
                            message
                        }}
                    }}
                }}
                }}
        """.format(
             video_url=video_url,
             organization_string=f"orgId: {organizarion_id}" if organizarion_id is not None else "",
             filename=filename)
        request_body={"query":graphql_query}
        headers={"Authorization":f"Bearer {token}"}
        resp=requests.post(self.api_url,json=request_body, headers=headers)
        if not resp.ok:
            print("Received bad resonse from graphql")
            return None
        # print('error handling in qery',resp.json())
        # try:
        #     token=resp.json()['data']['session']['createWithPassword']['sessionTokens']['accessToken']
        #     return token
        # except Exception:
        #     print("cant parse answer from graphql, when trying to get token")
        #     return None
        return resp.text