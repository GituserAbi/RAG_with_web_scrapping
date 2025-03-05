from constants import *

class Webscrape():
    def __init__(self, query, num_links=2):
        self.query = query
        self.num_links = num_links
    
    def method_get_article_url_links(self):
        """
        Uses googlesearch to find Towards Data Science articles for the given query.
        """
        search_query = f"site:towardsdatascience.com {self.query}"
        links = [url for url in search(search_query, num_results=self.num_links)]
        return links

    def method_scrape_articles(self, url):
        """
        Scrapes a Towards Data Science article, extracting the title and content.
        """
        driver.get(url)
        time.sleep(5)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content_list = [p.text.strip() for p in paragraphs if p.text.strip()]

        content = "\n".join(content_list)
        return content

    def method_store_data_text(self):
        urls = self.method_get_article_url_links()

        if not urls:
            print("No relevant articles found on Towards Data Science.")
        else:
            scraped_data = []
            for url in urls:
                print(f"Scraping -> {url}")
                result = self.method_scrape_articles(url)
                scraped_data.append(result)

            with open(text_file_path, "w", encoding="utf-8") as file:
                for data in scraped_data:
                    file.write(data + "\n\n")

            print(f"Scraping completed. Data saved to '{text_file_path}'.")
        driver.quit()

class VectorStore():
    def __init__(self):
        self.text_file_path = text_file_path
    
    def method_vector_store_text(self):
        loader = TextLoader(self.text_file_path, encoding="utf-8")
        documents = loader.load()
        vector_store.add_documents(documents = documents)
        vector_store.save_local(local_vectore_store_path)
        print(f"Succesfully Created the Vector Store!! for uploaded {self.text_file_path} file")
        return True

class RAG():
    def __init__(self, user_query, top_k=2):
        self.top_k = top_k
        self.user_query = user_query

    def method_retrieve_context(self):
        if os.path.exists(local_vectore_store_path):
            relevant_docs = vector_store.similarity_search(query = self.user_query, k=self.top_k)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            return context
        else:
            return "There is no Vector DB for retrieval"

    def method_generate_response(self):
        context = self.method_retrieve_context()
        prompt = f"""
        Your a Chat Assistant, you will understand the query and use the context to answer precisely.
        NOTE: If the context provided is not relevant to the Query then respond "NOT RELEVANT" and nothing else in your response.
        Query : {self.user_query}
        Context : {context}"""
        response = llm_model.generate_content(prompt)
        return response.text