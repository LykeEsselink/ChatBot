"""
This file contains the code necessary for training our Watson discovery environment with the Watson discovery API.
The send_query function can be used to send a natural language query to watson.
The relevance of the results must then be rated manually and submitted to watson
with the send_relevancy function. The example queries come from the watson_questions.txt file.
"""

import os
import json
import nltk
import requests
from watson_developer_cloud import DiscoveryV1

def send_query(user_query):
    discovery = DiscoveryV1(
        version="2018-03-05",
        username="044cea39-4515-404b-a5c1-3e7b216e1635",
        password="RK5rIKZ01yIf"
    )
    #, return_fields='text'
    my_query = discovery.query(environment_id='26410a73-bf30-47c5-85cb-538a14797fd2',
                                collection_id='fb1465fc-5731-4e56-9028-fac58374b638',
                                natural_language_query=user_query, return_fields=['text', 'level', 'keywords','url'],
                                passages_fields=['text'],
                                passages=True,
                                deduplicate_field='document_id',
                                count=1)



    qr1 = json.loads(json.dumps(my_query, indent=2))
    #print(qr1['matching_results'])
    #print(qr1['passages'][0])
    st = []
    for dicts in qr1['passages']:
        st.append(['QUERY: ' + user_query, 'SCORE: ' + str(dicts['passage_score']), 'TEXT: ' + dicts['passage_text'], 'DOC ID:' + dicts['document_id']])
    return(st)

wq = open('watson_questions').read()
wq = nltk.sent_tokenize(wq)
for questions in wq:
    print(questions)
    print('\n')

# GEBRUIK DEZE VOOR HET BEPALEN VAN RELEVANCY, HIER ZITTEN DE TEKSTEN EN DOCUMENT IDs IN
query_responses = [None] * 52
for i, sents in enumerate(wq):
    query_responses[i] = send_query(sents)


# PASSAGES ---- PASSAGES ---- PASSAGES ---- PASSAGES ---- PASSAGES ---- PASSAGES ---- PASSAGES ---- PASSAGES ---- # PASSAG
for questions in query_responses:
    print("------------------------------------------------------------------------------------------")
    for stuff in questions:
        print("\n")
        print(stuff)

def send_relevancy(query, articleid1, relevancy1, articleid2, relevancy2):
    headers = {
    'Content-Type': 'application/json',
    }

    params = (
        ('version', '2018-03-05'),
    )

    data = '\n{\n  "natural_language_query": '+'"'+ query +'"'+',\n  "examples": [\n    {\n      "document_id": ' + '"' + articleid1 + '"' + ',\n      "relevance": '+relevancy1+'\n    },\n    {\n      "document_id": ' + '"' + articleid2 + '"' + ',\n      "relevance": '+relevancy2+'\n    }\n  ]\n}'
    print(data)
    response = requests.post('https://gateway.watsonplatform.net/discovery/api/v1/environments/26410a73-bf30-47c5-85cb-538a14797fd2/collections/fb1465fc-5731-4e56-9028-fac58374b638/training_data', headers=headers, params=params, data=data, auth=('044cea39-4515-404b-a5c1-3e7b216e1635', 'RK5rIKZ01yIf'))
    return(response.content)
