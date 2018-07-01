# ChatBot
GitHub for a second year AI project at the University of Amsterdam (UvA). The project is about building a chatbot, specifically the back-end of a chatbot. The UvA wants to have a question-answering mechanism in the form of a chatbot, because the UvA search engine returns too many search results. The goal of this project is to be able to return only one URL of the correct webpage that contains the answer to the question of the user. 

We've experimented with three different possible solutions. First, we made a hierarchical tree structure and put all the A-Z pages into the right levels in that structure. When given a query, it will return the matching results based on keywords and a cosine similarity. Second, we used the UvA search engine and calculated the cosine similarity based on keywords of the top five search results. Lastly, we trained the Watson API on a database consisting of the general A-Z page and some studies. Watson returns a passage of the article and the URL.

Project team: Dorian Bekaert, Lyke Esselink, Mats Gonggrijp, Celine Kattenberg, Iris Lau and Carmen Timmerman
