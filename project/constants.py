import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import yaml
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from googlesearch import search

import faiss
import google.generativeai as genAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.document_loaders import TextLoader

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

chromedriver_path = config["CHROMEDRIVER_PATH"]
files_dir_name = config["FILES_DIRECTORY_NAME"]
text_file_name = config["TEXT_FILE_NAME"]
text_file_path = os.path.join(files_dir_name, text_file_name)
local_vectore_store_name = config["LOCAL_VECTOR_STORE_NAME"]
local_vectore_store_path = os.path.join(files_dir_name, local_vectore_store_name)
gemini_api_key = config["GEMINI_API_KEY"]
gemini_model_name = config["GEMINI_MODEL_NAME"]
embedding_model_name = config["EMBEDDING_MODEL_NAME"]

if not os.path.exists(files_dir_name):
    os.mkdir(files_dir_name)

# Set up Chrome WebDriver
service = Service(chromedriver_path)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Embedding Model Initialization
embedding_function = HuggingFaceEmbeddings(model_name=embedding_model_name)

# LLM Model Initialization
genAI.configure(api_key = gemini_api_key)
llm_model = genAI.GenerativeModel(gemini_model_name)

# Vector Store Inizialization
if os.path.exists(local_vectore_store_path):
    vector_store = FAISS.load_local(
        folder_path = local_vectore_store_path,
        embeddings = embedding_function,
        allow_dangerous_deserialization=True
    )
else:
    index = faiss.IndexFlatL2(len(embedding_function.embed_query("hello world")))
    vector_store = FAISS(
        embedding_function=embedding_function,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        distance_strategy = DistanceStrategy.COSINE
    )