"""
This file contains an interface with which out Watson discovery environment can be accessed.
The frontend_backend_interface function takes in a dictionary from the "front-end" group and returns a list of dictionaries: 
one dictionary for each URL returned by Watson discovery.
"""

# Imports
import os
import json
import nltk
import requests
from watson_developer_cloud import DiscoveryV1


# Helper functions

# Extracts the passage with the highest score for each of the pages returned by Watson
def get_passage(passages_list, doc_id):
    for passage_dict in passages_list:
        if passage_dict['document_id'] == doc_id:
            return passage_dict['passage_text']

    return("No passage was found for this document.")

# Adds a bonus if page is from the right level in the document hierarchy
def add_bonus(s, p):
    m = 1 - s
    b = p * m
    return(s+b)

# Interface
def frontend_backend_interface(input_dict):
    discovery = DiscoveryV1(
        version="2018-03-05",
        username="044cea39-4515-404b-a5c1-3e7b216e1635",
        password="RK5rIKZ01yIf"
    )
    # Get the natural language query
    user_query = input_dict["Source"]
    
    # See if the query is in Dutch or in English
    if input_dict['Language'] == 0: # Nederlands
        collection_id = '6e027bae-6639-4815-9189-08ba8518f65f'
    else:
        collection_id = 'fb1465fc-5731-4e56-9028-fac58374b638' # Engels
        
    # Send the query to the Watson discovery service with the discovery API
    my_query = discovery.query(environment_id='26410a73-bf30-47c5-85cb-538a14797fd2',
                                collection_id=collection_id,
                                natural_language_query=user_query, return_fields=['text', 'level', 'keywords','url'],
                                passages_fields=['text'],
                                passages=True,
                                deduplicate_field='document_id',
                                count=5) # Return a list of 5 dictionaries

    qr1 = json.loads(json.dumps(my_query, indent=2))

    # Create the output list of dictionaries (1 dictionary for each returned page)
    output_list = []
    # Add the dictionaries
    pages_dict = qr1['results'] #from here we get the url and scores
    for i in range(0, len(pages_dict)):
        keywords = qr1['results'][i]['keywords']
        if "confidence" in qr1['results'][i]['result_metadata']:
            confidence = qr1['results'][i]['result_metadata']['confidence']
        else:
            confidence = qr1['results'][i]['result_metadata']['score']
            confidence = (confidence/(4+confidence))
            
        level =  qr1['results'][i]['level']
        url = qr1['results'][i]['url']
        doc_id = qr1['results'][i]['id']

        if input_dict["Level"] in level:
            confidence = add_bonus(confidence, 0.5)

        # Create dictionary with the url, score, level, keywords and document id of the page
        page_dict = {"URL": url, "Score": confidence, "Level": level, "Keywords": keywords, "ID": doc_id}#, "Answer": passage}

        output_list.append(page_dict)

    # Put in a passage for a document if there is one
    for page in output_list:
        # Look for a passage
        passage = get_passage(qr1['passages'], page["ID"])
        page.pop('ID', None)
        page["Answer"] = passage

    # Sort the list based on confidence score
    output_list = sorted(output_list, key=lambda k: k['Score'], reverse=True)

    return(output_list)
