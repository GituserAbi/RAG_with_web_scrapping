# **Web Scraping + RAG (Retrieval-Augmented Generation) System**

## **Overview**
This project integrates **web scraping**, **vector indexing (FAISS)**, and **retrieval-augmented generation (RAG)** to fetch, store, and retrieve relevant content from online sources. It uses:
- **Selenium** - Automated web scraping
- **FAISS** - Similarity-based text retrieval
- **Google Gemini API** - AI-based response generation (LLM)
- **Streamlit** - Chatbot UI with human-in-the-loop (HITL) validation

---

## **Features**
- Automated web scraping for relevant articles  
- AI-driven response generation using Gemini API  
- Vector-based similarity search with FAISS  
- Human-in-the-loop validation for response accuracy  
- Lightweight and efficient chatbot interface (Streamlit)  

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo-url.git
cd your-repo
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Configuration**
Update **`config.yaml`** with required paths and API keys:
```yaml
CHROMEDRIVER_PATH : "C:\\ChromeDriver\\chromedriver.exe"
FILES_DIRECTORY_NAME : "files"
TEXT_FILE_NAME : "contents.txt"
EMBEDDING_MODEL_NAME : "all-MiniLM-L6-v2"
GEMINI_MODEL_NAME : "gemini-1.5-flash"
GEMINI_API_KEY : "your-gemini-api-key"
LOCAL_VECTOR_STORE_NAME : "faiss_index"
```

### **4. Run the Application**
Start the chatbot UI with:
```bash
streamlit run app.py
```

---

## **Project Structure**
```
├── config.yaml              # Configuration file
├── constants.py             # Global variables and model initialization
├── utils.py                 # Web scraping, vector store, and RAG implementation
├── main.py                  # Core logic for response generation
├── app.py                   # Streamlit UI for chatbot
├── requirements.txt         # Required Python dependencies
└── README.md                # Project documentation
```

---


