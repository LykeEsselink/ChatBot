import os
import json
from watson_developer_cloud import DiscoveryV1

def send_query(user_query):
    discovery = DiscoveryV1(
        version="2018-03-05",
        username="044cea39-4515-404b-a5c1-3e7b216e1635",
        password="RK5rIKZ01yIf"
    )
    #, return_fields='text'
    my_query = discovery.query(environment_id='26410a73-bf30-47c5-85cb-538a14797fd2',
                                collection_id='d18f374c-3852-4410-9863-2f91496898a1',
                                query=user_query, return_fields=['passage_text'],
                                passages=True,
                                count=1)




    return(json.dumps(my_query, indent=2))
