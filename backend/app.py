from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from flask_cors import CORS


# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")
genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            if page:
                text += page.extract_text() or ""
    return text
#The uploaded PDFs are read using the PdfReader class from a PDF processing library.
# The function iterates through the pages of each PDF and extracts text using page.extract_text().
# All the extracted text is concatenated into a single string.

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)
# The raw text is split into smaller chunks using RecursiveCharacterTextSplitter.
# Parameters like chunk_size (10,000 characters) and chunk_overlap (1,000 characters) ensure that:
# Description: The chunk_overlap parameter controls how much text from one chunk overlaps with the next. It ensures that consecutive chunks share some content, maintaining context between them.

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
# Each chunk is converted into an embedding vector using the GoogleGenerativeAIEmbeddings model. These embeddings capture the semantic meaning of the text.
# The chunks and their embeddings are stored in a FAISS vector store.

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. 
    If the answer is not in the provided context, just say, "Answer is not available in the context."
    
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)
# temperature=0.3: In natural language processing (NLP), temperature controls the randomness of the model's output. A lower value (like 0.3) makes the model's responses more deterministic and focused, while a higher value (like 0.7 or 1.0) would make it more creative and varied.
# Routes
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        files = request.files.getlist('pdf_files')
        if not files:
            return jsonify({"error": "No files uploaded"}), 400
        
        raw_text = get_pdf_text(files)
        if not raw_text.strip():
            return jsonify({"error": "No text extracted from PDFs"}), 400
        
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        print(raw_text)
        return jsonify({"message": "Files processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# LLM LangChain:
# A framework designed to simplify the use of LLMs by combining multiple tools and workflows.
@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        print("Received request at /ask_question")
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        question = data.get("question")
        print(f"Question received: {question}")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Loading FAISS index...")
        # Initializes the embedding model (embedding-001) using GoogleGenerativeAIEmbeddings. This model likely converts the question into a numerical format (embedding) for similarity comparisons.
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        # Loads a FAISS (Facebook AI Similarity Search) index from the local file system (faiss_index).
        # Serialization converts objects (e.g., embeddings and FAISS indices) into a storable format, such as binary or JSON.
        docs = new_db.similarity_search(question)

        if not docs:
            print("No relevant context found for the question")
            return jsonify({"error": "No relevant context found for the question"}), 404

        print("Context found, running conversational chain...")
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

        answer = response.get("output_text", "No response generated")
        print(f"Answer generated: {answer}")
        return jsonify({"answer": answer}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
