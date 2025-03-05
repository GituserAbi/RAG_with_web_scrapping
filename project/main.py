from utils import Webscrape, VectorStore, RAG

def generateResponse(prompt, top_k_contexts=2, num_links_to_scrape=2):
    rag_agent = RAG(user_query=prompt, top_k=top_k_contexts)
    response = rag_agent.method_generate_response().strip()

    if response == "NOT RELEVANT":
        web_scrapper = Webscrape(query=prompt, num_links=num_links_to_scrape)
        web_scrapper.method_store_data_text()

        vector_store = VectorStore()
        vector_store.method_vector_store_text()

        rag_agent = RAG(user_query=prompt, top_k=top_k_contexts)
        response = rag_agent.method_generate_response()            

    return response